#!/usr/bin/python

import sys
import os

import unittest


class Argument(object):
    """Holder information about argument"""

    def __init__(self, name):
        super(Argument, self).__init__()
        self.name = name
        self.required = False
        self.type = None
        self.num_args = None
        self.description = 'missing description'


class MySimpleParser(object):
    """A simple command-line arguments parser

    Accepts the next arguments patterns:
    --option                       =>    {'option': True, ...}
    --option=value                 =>    {'option': 'value', ...}
    --option value                 =>    {'option': 'value', ...}
    --option value1 value2         =>    {'option': [value1, value2], ...}

    """

    def __init__(self, prefix_chars='--'):
        super(MySimpleParser, self).__init__()
        self.prefix_chars = prefix_chars
        self.len_prefix_chars = len(prefix_chars)
        self.args_dict = {}

    def add_argument(self, name, **kwargs):
        if self.args_dict.has_key(name):
            raise ValueError(
                'Argument with name {} already exists.'.format(name))

        argument = Argument(name)

        if kwargs.has_key('required'):
            argument.required = kwargs['required']
        else:
            argument.required = False

        if kwargs.has_key('type'):
            argument.type = kwargs['type']
        else:
            argument.type = None

        if kwargs.has_key('description'):
            argument.description = kwargs['description']
        else:
            argument.description = 'missing description'

        if kwargs.has_key('num_args'):
            argument.num_args = kwargs['num_args']
        else:
            argument.num_args = None

        self.args_dict[argument.name] = argument

    def get_usage(self, arg):
        required_args = ''
        if arg.type == bool:
            required_args = '--' + arg.name + ''
        else:
            required_args = '--' + arg.name + '=<value>'
        return required_args

    def is_help(self, args):
        for arg in args:
            if arg.startswith(self.prefix_chars):
                key = arg[self.len_prefix_chars:]
                if key == 'help':
                    usage = 'usage: ' + os.path.basename(__file__) + ' '
                    required_args = ''
                    options_args = ''
                    required_description = ''
                    options_description = ''
                    template_desc = "    {0:12} {1:12}\n"
                    for name in self.args_dict:
                        option = self.args_dict[name]
                        if option.required:
                            required_args = required_args + \
                                self.get_usage(option) + ' '
                            required_description = required_description + \
                                template_desc.format(name, option.description)
                        else:
                            options_args = options_args + \
                                '[' + self.get_usage(option) + '] '
                            options_description = options_description + \
                                template_desc.format(name, option.description)

                    usage = usage + required_args + options_args + \
                        '\n\n' + required_description + options_description
                    print(usage)
                    return True
        return False

    def parse_args(self, args=sys.argv[1:]):
        if self.is_help(args):
            return

        res_dict = {}
        key = ''
        for arg in args:
            if arg.startswith(self.prefix_chars):
                split = arg[self.len_prefix_chars:].split('=')
                if len(split) > 1:
                    key, value = split[0], split[1:]
                    if len(value) > 1:
                        raise ValueError(
                            'Too many "{}" in argument: {}'.format('=', arg))

                    if not res_dict.has_key(key):
                        res_dict[key] = []
                    if value[0]:
                        res_dict[key].append(value[0])

                else:
                    key = arg[self.len_prefix_chars:]
                    if not res_dict.has_key(key):
                        res_dict[key] = []
            elif key:
                res_dict[key].append(arg)

        self.check_args(res_dict)

        return res_dict

    def check_args(self, res_dict):
        for key in res_dict:
            if not self.args_dict.has_key(key):
                raise ValueError('Unknown argument: <{}>.'.format(key))

        for key in self.args_dict:
            arg = self.args_dict[key]
            if res_dict.has_key(arg.name):
                if arg.type:
                    value = res_dict[arg.name]
                    if arg.type == bool:
                        if value:
                            if value[0] == 'False' or value[0] == 'false':
                                res_dict[arg.name] = False
                            else:
                                res_dict[arg.name] = True
                        else:
                            res_dict[arg.name] = True

                    elif value:
                        if arg.num_args:
                            if len(value) != arg.num_args:
                                raise ValueError('For option <{}> required num_args <{}> was not supplied.'.format(
                                    arg.name, arg.num_args))
                        value = res_dict[arg.name]
                        if len(value) > 1:
                            cast_value = []
                            for i in value:
                                cast_value.append(arg.type(i))
                            res_dict[arg.name] = cast_value
                        else:
                            res_dict[arg.name] = arg.type(value[0])
                    elif arg.num_args:
                        raise ValueError('For option <{}> required num_args <{}> was not supplied.'.format(
                            arg.name, arg.num_args))

            elif arg.required:
                raise ValueError(
                    'Required argument <{}> was not supplied.'.format(arg.name))


class TestMySimpleParser(unittest.TestCase):
    """tests for MySimpleParser"""

    def test_for_duplicate_argument(self):
        parser = MySimpleParser()
        parser.add_argument('arg', type=int, required=True,
                            description='argument type int')

        with self.assertRaises(ValueError):
            parser.add_argument('arg')

    def test_for_unknown_argument(self):
        parser = MySimpleParser()

        with self.assertRaises(ValueError):
            parser.parse_args(['--foo=123'])

        with self.assertRaises(ValueError):
            parser.parse_args(['--foo'])

    def test_for_required_argument(self):
        parser = MySimpleParser()

        parser.add_argument('arg1', type=int, required=True)
        parser.add_argument('arg2', type=int, required=True)

        with self.assertRaises(ValueError):
            parser.parse_args([])

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg1=111'])

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg2=222'])

        self.assertDictEqual(parser.parse_args(
            ['--arg1=111', '--arg2=222']), eval("{'arg1':111,'arg2':222}"))

    def test_for_bool_argument(self):
        parser = MySimpleParser()
        parser.add_argument('arg1', type=bool, required=True)

        self.assertDictEqual(parser.parse_args(
            ['--arg1']), eval("{'arg1':True}"))

        self.assertDictEqual(parser.parse_args(
            ['--arg1=True']), eval("{'arg1':True}"))

        self.assertDictEqual(parser.parse_args(
            ['--arg1=False']), eval("{'arg1':False}"))

        self.assertDictEqual(parser.parse_args(
            ['--arg1=false']), eval("{'arg1':False}"))

    def test_for_int_argument(self):
        parser = MySimpleParser()
        parser.add_argument('arg', type=int, required=True,
                            description='argument type int')

        self.assertDictEqual(parser.parse_args(
            ['--arg=123']), eval("{'arg':123}"))
        self.assertDictEqual(parser.parse_args(
            ['--arg', '123']), eval("{'arg':123}"))

        with self.assertRaises(ValueError):
            parser.parse_args([])

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg=26682216422L'])

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg=123.123'])

    def test_for_long_argument(self):
        parser = MySimpleParser()
        parser.add_argument('arg', type=long, required=True,
                            description='argument type long')

        self.assertDictEqual(parser.parse_args(
            ['--arg=26682216422L']), eval("{'arg':26682216422L}"))
        self.assertDictEqual(parser.parse_args(
            ['--arg', '26682216422L']), eval("{'arg':26682216422L}"))

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg=123.123'])

    def test_for_float_argument(self):
        parser = MySimpleParser()
        parser.add_argument('arg', type=float, required=True,
                            description='argument type long')

        self.assertDictEqual(parser.parse_args(
            ['--arg=123']), eval("{'arg':123}"))
        self.assertDictEqual(parser.parse_args(
            ['--arg=123.123']), eval("{'arg':123.123}"))

        self.assertDictEqual(parser.parse_args(
            ['--arg', '123']), eval("{'arg':123}"))
        self.assertDictEqual(parser.parse_args(
            ['--arg', '123.123']), eval("{'arg':123.123}"))

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg=26682216422L'])

    def test_for_str_argument(self):
        parser = MySimpleParser()
        parser.add_argument('arg', type=str, required=True,
                            description='argument type long')

        self.assertDictEqual(parser.parse_args(
            ['--arg=123']), eval("{'arg':'123'}"))
        self.assertDictEqual(parser.parse_args(
            ['--arg=26682216422L']), eval("{'arg':'26682216422L'}"))
        self.assertDictEqual(parser.parse_args(
            ['--arg=123.123']), eval("{'arg':'123.123'}"))
        self.assertDictEqual(parser.parse_args(
            ['--arg=world']), eval("{'arg':'world'}"))

        self.assertDictEqual(parser.parse_args(
            ['--arg', '123']), eval("{'arg':'123'}"))
        self.assertDictEqual(parser.parse_args(
            ['--arg', '26682216422L']), eval("{'arg':'26682216422L'}"))
        self.assertDictEqual(parser.parse_args(
            ['--arg', '123.123']), eval("{'arg':'123.123'}"))
        self.assertDictEqual(parser.parse_args(
            ['--arg', 'world']), eval("{'arg':'world'}"))

    def test_for_eval_argument(self):
        parser = MySimpleParser()
        parser.add_argument('arg', type=eval, required=True,
                            description='argument type long')

        self.assertDictEqual(parser.parse_args(["--arg={'name':'Alex', 'age':18, 'married':False}"]), eval(
            "{'arg': {'name':'Alex', 'age':18, 'married':False} }"))
        self.assertDictEqual(parser.parse_args(["--arg", "{'name':'Alex', 'age':18, 'married':False}"]), eval(
            "{'arg': {'name':'Alex', 'age':18, 'married':False} }"))

    def test_for_list_values(self):
        parser = MySimpleParser()
        parser.add_argument('arg1', type=int, required=False)
        parser.add_argument('arg2', type=int, required=False)

        self.assertDictEqual(parser.parse_args(
            ['--arg1', '1', '2', '3', '4', '--arg2', '11', '22']), eval("{'arg1':[1,2,3,4], 'arg2':[11,22]}"))

        self.assertDictEqual(parser.parse_args(
            ['--arg1=1', '2', '3', '4', '--arg2=11', '22']), eval("{'arg1':[1,2,3,4], 'arg2':[11,22]}"))

    def test_for_def_num_args(self):
        parser = MySimpleParser()
        parser.add_argument('arg1', type=int, num_args=3, required=True)

        self.assertDictEqual(parser.parse_args(
            ['--arg1', '1', '2', '3']), eval("{'arg1':[1,2,3]}"))

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg1', '1'])

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg1', '1', '2'])

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg1', '1', '2', '3', '4'])

    def test_complex(self):
        parser = MySimpleParser()
        parser.add_argument('arg_int', type=int, required=True,
                            num_args=2, description='help description for arg_int ')
        parser.add_argument('arg_str', type=str, required=True,
                            description='help description for arg_str')
        parser.add_argument('arg_eval', type=eval, required=False,
                            description='help description for arg_eval')
        parser.add_argument('arg_bool', type=bool, required=False,
                            description='help description for arg_bool')
        parser.add_argument('arg_float', type=float, required=False,
                            description='help description for arg_float')

        self.assertDictEqual(parser.parse_args(['--arg_int', '1', '2', '--arg_str', 'good', '--arg_eval',
                                                '{"name":"Alex", "age":18}', '--arg_bool', '--arg_float', '3.14']), eval(
            "{'arg_int': [1, 2], 'arg_str': 'good', 'arg_eval': {'age': 18, 'name': 'Alex'}, 'arg_bool': True, 'arg_float': 3.14 }"))

        self.assertDictEqual(parser.parse_args(['--arg_int', '1', '2', '--arg_str', 'good']), eval(
            "{'arg_int': [1, 2], 'arg_str': 'good'}"))

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg_int', '1', '--arg_str', 'good', '--arg_eval',
                               '{"name":"Alex", "age":18}', '--arg_bool', '--arg_float', '3.14'])

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg_int', '1'])

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg_int', '1', '2'])

        with self.assertRaises(ValueError):
            parser.parse_args(['--arg_str', 'good'])


# Self-test
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMySimpleParser)
    unittest.TextTestRunner().run(suite)
