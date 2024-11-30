var = 6;

match (var):
    case 0:
        print('0')
    case 2:
        print('2')
    case _: # _ means default
        print('3')