import math
import time
import random
import csv
import matplotlib.pyplot as plt
import numpy as np

from Node import OurNode, HDNDNode, RandomNode, MLENode
import utils
from visualize import visualize_network
from typing import List


data = []   # 存放实验数据


def create_ournodes(num=10, P=[3, 5, 7], scope=3, radius=15, cover=120, angle_offset=False, time_offset=False):
    '''
    随机生成num个OurNode：
    1. 节点坐标随机，但保证无孤立节点
    2. 质数p遵循分布P
    3. 节点的启动时间可控（一致或有偏差）
    4. 节点的正北朝向可控（一致或有偏差）
    5. 通信半径为radiuse
    6. 覆盖范围为cover
    '''
    nodes = []

    coordinates = utils.generate_coordinates(num, radius, scope)
    #coordinates = utils.read_coordinates(str(num) + '.txt')

    extend_P = P * (num // len(P)) + P[:num % len(P)] if len(P) < num else P
        
    for i, (x, y) in enumerate(coordinates):
        offset1 = random.randrange(0, 91, 10) if angle_offset else 0
        offset2 = random.randrange(0, 10) if time_offset else 0
        node = OurNode(x, y, scope, radius, cover, offset1, offset2, extend_P[i], P)
        nodes.append(node)

    return nodes


def create_hdndnodes(num=10, P=[3, 5, 7], scope=3, radius=15, cover=120, angle_offset=False, time_offset=False):
    nodes = []

    #coordinates = utils.generate_coordinates(num, radius, scope)
    coordinates = utils.read_coordinates('temp-' + str(num) + '.txt')
    ids = utils.generate_ids(num, 6)

    for (x, y), id in zip(coordinates, ids):
        offset1 = random.randrange(0, 91, 10) if angle_offset else 0
        offset2 = random.randrange(0, 10) if time_offset else 0
        node = HDNDNode(x, y, scope, radius, cover, offset1, offset2, P[0], P[2], id)
        nodes.append(node)

    return nodes


def create_randomnodes(num=10, scope=3, radius=15, cover=120, angle_offset=False, time_offset=False):
    nodes = []

    #coordinates = utils.generate_coordinates(num, radius, scope)
    coordinates = utils.read_coordinates('temp-' + str(num) + '.txt')
    
    for x, y in coordinates:
        node = RandomNode(x, y, scope, radius, cover, angle_offset, time_offset)
        nodes.append(node)

    return nodes


def create_mlenodes(num=10, scope=3, radius=15, cover=120, angle_offset=False, time_offset=False):
    nodes = []

    #coordinates = utils.generate_coordinates(num, radius, scope)
    coordinates = utils.read_coordinates('temp-' + str(num) + '.txt')
    
    for x, y in coordinates:
        offset1 = random.randrange(0, 91, 10) if angle_offset else 0
        offset2 = random.randrange(0, 10) if time_offset else 0
        node = MLENode(x, y, scope, radius, cover, offset1, offset2)
        nodes.append(node)

    return nodes


def count(cur_time, nodes, complete_nodes):
    rates = []
    for i, node in enumerate(nodes):
        total, cnt = node.count_neighbors()
        rate = cnt / total if total > 0 else 1
        if rate >= 1 and node not in complete_nodes:
            print(f'Time:  {cur_time}\t Node {i} completes!\t'
                  f'Total: {total}\t Count: {cnt}\t Rate: {rate:.2f}')
            complete_nodes.add(node)
            data.append([i + 1, total, cnt, rate, cur_time])

        rates.append(rate)

    avg_rate = sum(rates) / len(rates)
    return avg_rate


def output_data(file_name):
    data.sort(key=lambda x: x[0])
    avg = np.mean(data, axis=0).tolist()
    avg[0] = '平均'
    
    sums = np.sum(data, axis=0).tolist()
    sums[0] = '总时间'
    sums[-1] = np.max([row[-1] for row in data])
    sums[-2] = avg[-2]
    
    data.append(avg)
    data.append(sums)

    with open(file_name, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

def main(args):
    # 参数获取
    exp = args.exp
    num_nodes = args.num
    interval = args.inter
    angle_offset = args.angle_offset
    time_offset = args.time_offset
    scope = args.scope
    radius = args.radius
    cover = args.cover
    
    # 随机数分布
    P: List[int] = utils.generate_p(num_nodes, cover, 1)
    total_time = max(2 * P[-1] * P[-2], int(1e5))    # 根据质数分布计算
    # P = [6, 7]

    # 节点生成
    nodes = []
    complete_nodes = set()
    if exp == 'our':
        nodes = create_ournodes(num_nodes, P, scope, radius, cover, angle_offset, time_offset)
    elif exp == 'hdnd':
        nodes = create_hdndnodes(num_nodes, P, scope, radius, cover, angle_offset, time_offset)
    elif exp == 'random':
        nodes = create_randomnodes(num_nodes, scope, radius, cover, angle_offset, time_offset)
    elif exp == 'mle':
        nodes = create_mlenodes(num_nodes, scope, radius, cover, angle_offset, time_offset)
    
    # 邻居初始化
    for node in nodes:
        node.find_neighbors(nodes)

    # 画布初始化
    fig = plt.figure(figsize=(10, 10))

    # 程序主体循环
    print(f'P: {P}')
    print(f'Total time: {total_time}')
    for i in range(total_time):
        # 可视化
        # visualize_network(nodes, fig)
        
        # 判断邻居关系
        for node in nodes:
            node.check_neighbors(i)

        # 更新节点朝向
        for node in nodes:
            node.update_orientation_status(i)

        # 统计邻居发现结果
        rate = count(i, nodes, complete_nodes)
        if rate >= 1:
            print(f'Discovering completed! Total time: {i}')
            break
            
        # 休眠一段时间
        time.sleep(interval)

    rate = count(total_time, nodes, complete_nodes)
    print(f'Time out! Rate: {rate}')
    print('Uncomplete nodes:')
    for i, node in enumerate(nodes):
        if node not in complete_nodes:
            total, cnt = node.count_neighbors()
            rate = cnt / total if total > 0 else 1
            print(f'Node: {i}\t Total: {total}\t Count: {cnt}\t Rate: {rate:.2f}')
            data.append([i + 1, total, cnt, rate, total_time])
            
    output_data(f'results/{num_nodes}_{exp}.csv')
          

if __name__ == "__main__":
    args = utils.get_args()
    main(args)
    
