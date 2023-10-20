


import random as r
c = 0
li = [0,1,2]
while c<1000:
    n = 1
    n+=1
    temp = li
    r.shuffle(temp)

    print(temp)
    if temp[1] != 1:
        temp.pop(1)
    elif temp[1] == 1:
        temp.pop(2)
  
    if temp[0] == 1:
        c += 1 

print(f'{c}/1000')