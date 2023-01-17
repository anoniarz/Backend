def f(number,bool):
    e = 0
    o = 0
    for symbol in str(number):
        if int(symbol)%2 == 0:
            e += int(symbol)
        elif int(symbol)%2 == 1:
            o += int(symbol)
    if bool == True:
        return(e)
    elif bool == False:
        return(o)
print(f(20576,0))