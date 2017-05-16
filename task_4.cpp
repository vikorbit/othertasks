#include <iostream>
#include <forward_list>
#include <vector>
#include <assert.h> 

template<typename _ForwardIterator>
void regrouping(_ForwardIterator it ) {
    std::vector< std::_Fwd_list_node_base * > vec_pointer;

    std::_Fwd_list_node_base * next = ( it._M_node );

    while ( next != nullptr ) {
        vec_pointer.push_back( next );
        next = ( next->_M_next );
    }

    int k = 0;
    int l = vec_pointer.size() - 1;

    while ( k < l ) {
        vec_pointer[ k ]->_M_next = vec_pointer[ l ];
        k = k + 1;
        vec_pointer[ l ]->_M_next = vec_pointer[ k ];
        l = l - 1;
    }

    vec_pointer[ k ]->_M_next = nullptr;
}

int main ()
{
    std::forward_list<int> data = { 1, 2, 3, 4, 5, 6, 7, 8 };

    regrouping( data.begin() );

    std::vector<int> result = { 1, 8, 2, 7, 3, 6, 4, 5 };
    auto it = data.begin();
    for ( auto & x : result ) {
        assert( x == *it );
        it++;
    }

    return 0;
}