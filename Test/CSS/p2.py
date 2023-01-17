# def binary_number(number):
#     number = str(number)
#     s = 0
#     for symbol in number:
#         if symbol != "0" and symbol != "1":
#             s+=1
#     if s > 0:
#         return False
#     else:
#         return True
# print(binary_number("101100"))

def monety(n):
    li = [5,2,1]
    while n>0:
        m = 0
        i=0
        if n/li[i]>1:
            m+=n//li[i]
            n = n - li[i] * n//li[i]
            i+=1
    return(m)
print(monety(213))

