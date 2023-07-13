import argparse
import random


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--num', type=int,
                           help='number of nodes', default=10)
    argparser.add_argument('--inter', type=int,
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
        id += '0' * (len(id) // 2 + 1) + '1' * ((len(id) + 1) // 2)
        ids.add(id)
    return list(ids)
