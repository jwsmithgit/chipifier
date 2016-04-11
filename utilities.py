def find_closest( list_, value ) :
    return min(list_, key=lambda x:abs(x-value))
