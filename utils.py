import argparse
import random


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--exp', type=str, choices=['our', 'hdnd', 'random', 'mle'],
                           help='node type', default='our')
    argparser.add_argument('--num', type=int,
                           help='number of nodes', default=10)
    argparser.add_argument('--inter', type=float,
                           help='rotation interval', default=3)
    argparser.add_argument('--angle_offset', type=bool,
                           help='offset of north angle', default=False)
    argparser.add_argument('--time_offset', type=bool,
                           help='offset of start time', default=False)
    argparser.add_argument('--scope', type=int,
                           help='movement scope radius', default=3)
    argparser.add_argument('--radius', type=int,
                           help='communication radius', default=15)
    argparser.add_argument('--cover', type=int,
                           help='coverage angle of transceiver', default=60)
    args = argparser.parse_args()
    return args


def generate_coordinates(num, radius, scope):
    coordinates = []
    coordinates.append((random.uniform(0, 100), random.uniform(0, 100)))  # 添加第一个坐标
    while len(coordinates) < num:
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        for coord in coordinates:
            distance = ((x - coord[0]) ** 2 + (y - coord[1]) ** 2) ** 0.5
            if distance + scope * 2 <= radius:
                coordinates.append((x, y))
                break

    with open(f'temp-{num}.txt', 'w') as file:
        for coord in coordinates:
            file.write(f'{coord[0]}, {coord[1]}\n')
    
    return coordinates


def read_coordinates(filename):
    coordinates = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = line.strip().split(',')
            coordinates.append((float(x), float(y)))
    return coordinates


def generate_ids(num, n):
    ids = set()
    while len(ids) < num:
        id = ''.join(random.choice(['0', '1']) for _ in range(n))
        ids.add(id)
    return list(ids)


def get_primes():
    '''
    线性筛求100以内的质数
    '''
    primes = []  # 存储所有素数
    st = [False] * 100  # 标记数是否被筛掉
    cnt = 0  # 素数个数
    
    for i in range(2, 100):
        if not st[i]:
            primes.append(i)
            cnt += 1

        for p in primes:
            if p * i >= 100:
                break

            st[p * i] = True
            if i % p == 0:
                break
    
    return primes

def generate_p(num, cover, threshold):
    primes = get_primes()
    for i, p in enumerate(primes):
        if 360.0 / p <= cover:
            primes = primes[i:i + num]
            break

    # print(primes)

    if threshold == 1:
        return primes, 2

    gamma = 2
    w = 0
    idx = 1   # 左右分割primes为P和Q两部分的下标
    while w < threshold:
        # print(f'idx-{idx} w-{w} lambda-{gamma}')
        if idx + 1 >= num or (idx + 1 < num and (1 - 1 / (idx + 1) ** gamma) >= threshold):
            break
        
        temp = gamma
        # while (1 - 1 / (idx + 1) ** temp) <= threshold:
        temp += 1
        idx += 1
        if temp > primes[idx]: idx += 1
        else: gamma = temp
        w = 1 - 1 / (idx + 1) ** gamma

    print(primes[:idx + 1], gamma)
    return primes[:idx + 1], gamma


if __name__ == "__main__":
    primes, gamma = generate_p(10, 60, 0.9)
    print(primes)
    print(gamma)
