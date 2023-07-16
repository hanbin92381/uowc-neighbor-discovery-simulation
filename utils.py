import argparse
import random
import math


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--exp', type=str, choices=['our', 'hdnd', 'random', 'mle'],
                           help='node type', default='our')
    argparser.add_argument('--num', type=int,
                           help='number of nodes', default=10)
    argparser.add_argument('--inter', type=float,
                           help='visualize interval', default=0)
    argparser.add_argument('--angle_offset', type=bool,
                           help='offset of north angle', default=False)
    argparser.add_argument('--time_offset', type=bool,
                           help='offset of start time', default=False)
    argparser.add_argument('--scope', type=int,
                           help='movement scope radius', default=5)
    argparser.add_argument('--radius', type=int,
                           help='communication radius', default=20)
    argparser.add_argument('--cover', type=int,
                           help='coverage angle of transceiver', default=120)
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
            if distance + scope * 2 < radius:
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
    st = [False] * 200  # 标记数是否被筛掉
    cnt = 0  # 素数个数
    
    for i in range(2, 200):
        if not st[i]:
            primes.append(i)
            cnt += 1

        for p in primes:
            if p * i >= 200:
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
        return primes

    w = 0
    idx = 1   # 左右分割primes为P和Q两部分的下标
    while w < threshold:
        # print(f'idx-{idx} w-{w} lambda-{gamma}')
        if idx + 1 >= num or (idx + 1 < num and (1 - 1 / (idx + 1)) >= threshold):
            break
        
        idx += 1
        w = 1 - 1 / (idx + 1)

    return primes[:idx + 1]


def reallocate_p(nodes):
    # 遍历一遍nodes 生成全局拓扑图

    # 生成node下标-度数的map 按照度数从高到低排序

    # 生成node下标-是否分配的map

    # 从
    pass

if __name__ == "__main__":
    primes = generate_p(40, 60, 0.9)
    print(primes)

    '''
    def generate_random_coordinate(center_x, center_y, radius):
        x = random.uniform(center_x - radius, center_x + radius)
        y_range = math.sqrt(radius**2 - (x - center_x)**2)
        y = random.uniform(center_y - y_range, center_y + y_range)
        return x, y

    
    x = 0
    y = 0
    r = 10
    for _ in range(10):
        a, b = generate_random_coordinate(x, y, r)
        print(a, b)
    '''
