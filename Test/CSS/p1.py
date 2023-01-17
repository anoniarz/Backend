import random
card_number=""
for i in range(16):
    card_number+=str(random.randrange(10))
print(f'{card_number[:2]}{"*"*10}{card_number[12:16]}')

