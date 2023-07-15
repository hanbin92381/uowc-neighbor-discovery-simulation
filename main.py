import math
import time
import random
import argparse
import matplotlib.pyplot as plt
from Node import OurNode, HDNDNode, RandomNode, MLENode
import utils
from visualize import visualize_network


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

    if len(P) < num:
        P = P * (num // len(P)) + P[:num % len(P)]
        
    for i, (x, y) in enumerate(coordinates):
        offset1 = random.randrange(0, 91, 10) if angle_offset else 0
        offset2 = random.randrange(0, 10) if time_offset else 0
        node = OurNode(x, y, scope, radius, cover, offset1, offset2, P[i])
        nodes.append(node)

    return nodes


def create_hdndnodes(num=10, p=3, q=5, scope=3, radius=15, cover=120, angle_offset=False, time_offset=False):
    nodes = []

    #coordinates = utils.generate_coordinates(num, radius, scope)
    coordinates = utils.read_coordinates(str(num) + '.txt')
    ids = utils.generate_ids(num, 6)

    for (x, y), id in zip(coordinates, ids):
        node = HDNDNode(x, y, scope, radius, cover, angle_offset, time_offset, p, q, id)
        nodes.append(node)

    return nodes


def create_randomnodes(num=10, scope=3, radius=15, cover=120, angle_offset=False, time_offset=False):
    nodes = []

    #coordinates = utils.generate_coordinates(num, radius, scope)
    coordinates = utils.read_coordinates(str(num) + '.txt')
    
    for x, y in coordinates:
        node = RandomNode(x, y, scope, radius, cover, angle_offset, time_offset)
        nodes.append(node)

    return nodes


def create_mlenodes(num=10, scope=3, radius=15, cover=120, angle_offset=False, time_offset=False):
    nodes = []

    #coordinates = utils.generate_coordinates(num, radius, scope)
    coordinates = utils.read_coordinates(str(num) + '.txt')
    
    for x, y in coordinates:
        node = MLENode(x, y, scope, radius, cover, angle_offset, time_offset)
        nodes.append(node)

    return nodes


def count(nodes):
    print('Start counting...')
    rates = []
    for i, node in enumerate(nodes):
        total_num = len(node.potential_neighbors)
        discovered_num = len(node.discovered_neighbors)
        rate = discovered_num / total_num if total_num > 0 else 1
        print(f'[Node {i}] discover neighbors: {discovered_num}/{total_num}\t'
              f'rate: {rate:.2f}')
        rates.append(rate)

    print(f'Average discovering rate: {sum(rates) / len(rates)}')


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
    P, gamma = utils.generate_p(num_nodes, cover, 0.95)
    total_time = P[-1] * P[-2]   # 应该根据质数分布计算
    # P = [6, 7]

    # 节点生成
    nodes = []
    if exp == 'our':
        nodes = create_ournodes(num_nodes, P, scope, radius, cover, angle_offset, time_offset)
    elif exp == 'hdnd':
        nodes = create_hdndnodes(num_nodes, 3, 5, scope, radius, cover, angle_offset, time_offset)
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
    for i in range(total_time * gamma):
        # 可视化
        visualize_network(nodes, fig)
        
        # 判断邻居关系
        for node in nodes:
            node.check_neighbors(i)

        # 更新节点朝向
        for node in nodes:
            node.update_orientation(i)

        # 重新分配p
        if exp == 'our' and i and i % total_time == 0:
            # print('reassign P')
            for node in nodes:
                node.p = random.choice(P)
            
        # 休眠一段时间
        time.sleep(interval)
    
    # 统计邻居发现结果
    count(nodes)

    # cal_time

    # 根据节点分布情况换用更合适的P
    # TODO
    

if __name__ == "__main__":
    args = utils.get_args()
    main(args)
    
