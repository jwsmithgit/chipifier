def find_closest( list_, value ) :
    return min(list_, key=lambda x:abs(x-value))
    
    '''
    if value < list_[0] :
        return list_[0]
    if value > list_[-1] :
        return list_[-1]

    mid = len(list_) // 2
    a = list_[ mid ]
    b = list_[ mid + 1 ]

    if value > a and value < b :
        a_diff = value - a
        b_diff = b - value
        if a_diff < b_diff :
            return a
        else :
            return b

    if value < a :
        return find_closest( list_[:mid], value )

    else :
        return find_closest( list_[mid:], value )
    '''
