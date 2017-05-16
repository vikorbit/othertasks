#!/usr/bin/python

import sys
import unittest

from sympy.ntheory import factorint
import time


def factors_natural_series(n):
    for i in xrange(2, n + 1):
        print('n={} factors={}'.format(i, factorint(
            i, use_trial=True, use_rho=True, use_pm1=True, verbose=False)))

if __name__ == '__main__':
    n = 2000001
    factors_natural_series(n)
