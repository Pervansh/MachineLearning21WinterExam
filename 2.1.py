import csv

# q - кол-во дней, которые обрабатываются
# Асимптотика: O(k^2 * q)

k: int = int(input('Enter K: '))
start: int = int(input('Enter start capital: '))

maxMoney: list[list[int]] = [[0 for j in range(k + 1)] for i in range(k + 1)] # [i][j] - Макс. доход при продаже акций с j до i
maxBase: list[list[int]] = [[-1 for j in range(k + 1)] for i in range(k + 1)] # [i][j] - Макс. основание при продаже акций с j до i.

maxBase[k][k] = start

reader = csv.reader(open('new.csv', "r"))

cnt = -1
maxPrice: int = 0
minPrice: int = 1e8
for row in reader:
    if (cnt == -1):
        cnt += 1
        continue
    
    num: int = int(row[0])
    date: int = int(row[1])
    time: int = int(row[2])
    price: int = int(float(row[3]))
    curMax: list[int] = [0 for i in range(k + 1)] # [i] - max(maxMoney[i][j]) для всех j >= i

    maxPrice = max(maxPrice, price)
    minPrice = min(minPrice, price)

    for i in range(k + 1):
        for j in range(i, k + 1):
            if (maxBase[i][j] == -1):
                continue

            maxMoney[i][j] = price * (j - i) + maxBase[i][j]
            curMax[i] = max(curMax[i], maxMoney[i][j])

    for i in range(k + 1):
        for j in range(i, k + 1):
            maxBase[i][j] = max(maxBase[i][j], curMax[j] + price * (i - j))

    cnt += 1

ans: int = 0
for i in range(k + 1):
        for j in range(i, k + 1):
            ans = max(ans, maxMoney[i][j])

print('Max money: {}'.format(ans))
print('Max profit: {}'.format(ans - start))
