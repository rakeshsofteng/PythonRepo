def box_print(symbol, width, height):
    if len(symbol) != 1:
       print("Length="+ str(len(symbol)))
       print("symbol="+ str(symbol))
       raise Exception('Symbol must be a single character string.')
    if width <= 2:
       raise Exception('Width must be greater than 2.')
    if height <= 2:
       raise Exception('Height must be greater than 2.')

    print(symbol * width)
    for i in range(height - 2):
        print(symbol + (' ' * (width - 2)) + symbol)
    print(symbol * width)

try:
    box_print('*', 10, 4)
    #box_print('O', 20, 5)
    #box_print('x', 10, 3)
    #box_print('Z', 10, 3)
except Exception as err:
   print('An exception happened: ' + str(err))

try:
    box_print('#', 10, 4)
except Exception as err:
    print('An exception happened: ' + str(err))