cards = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}


def points(hand):
    import collections as co

    hand = hand.split(" ")

    order = []
    colors = []

    for h in hand:

        colors.append(h[1])
        order.append(int(cards[h[0]]))

    order.sort()
    count = co.Counter(order)
    print(count)
    if all(order[i] == order[i+1]+1 for i in range(len(order))) and len(set(colors)) == 1:
        return [order[4], 10]
    # elif max(count.values() == 4):
    #     hc = count.values().index(4)
    #     points = 9

    # elif any([order[0] == order[2] and order[3] == order[4], order[0] == order[1] and order[2] == order[4]]):
    #     points = 8

    # elif len(set(colors)) == 1:
    #     points = 7

    # elif all([order[i] == order[i+1]+1 for i in range(len(order))]):
    #     points = 6

    # return [points, hc]


print(points("2H 3H 4H 5H 6H"))
