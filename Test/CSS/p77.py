def bonus(y):
    b = 0
    if y > 8:
        b+=(y-8)*50
        y=y-8
    elif y > 5:
        b+=(y-5)*200
        y=y-5
    elif y>0:
        b+=(y)*100
    return(b)

print(bonus(9))
        