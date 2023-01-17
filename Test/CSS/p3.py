def amount_to_pay(money):
    s = 0
    s2 = 0
    s+=money//5
    money = money - s*5
    s2+=money//2
    money = money - s2*2
    sum = s+s2+money
    print(sum)
amount_to_pay(231)
