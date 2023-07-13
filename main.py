import math
import time
import random
import argparse
import matplotlib.pyplot as plt
from Node import OurNode, HDNDNode
import utils
from visualize import visualize_network


def create_ournodes(num=10, P=[3, 5, 7], angle_offset=False, time_offset=False, scope=3, radius=15, cover=120):
    '''
    随机生成num个OurNode：
    1. 节点坐标随机，但保证无孤立节点
    2. 质数p遵循分布P
    3. 节点的启动时间可控（一致或有偏差）
    4. 节点的正北朝向可控（一致或有偏差）
    5. 通信半径为radius
    6. 覆盖范围为cover
    '''
    nodes = []

    coordinates = utils.generate_coordinates(num, radius, scope)
    # coordinates = utils.read_coordinates(num_nodes + '.txt)

    for x, y in coordinates:
        p = random.choice(P)
        offset1 = random.randrange(0, 91, 10) if angle_offset else 0
        offset2 = random.randrange(0, 10) if time_offset else 0
        node = OurNode(x, y, scope, radius, cover, p, offset1, offset2)
        nodes.append(node)

    return nodes


def create_hdndnodes(num=10, p=3, q=5, scope=3, radius=15, cover=120):
    nodes = []

    coordinates = utils.generate_coordinates(num, radius, scope)
    # coordinates = utils.read_coordinates(num_nodes + '.txt)
    ids = utils.generate_ids(num, 6)

    for (x, y), id in zip(coordinates, ids):
        node = HDNDNode(x, y, scope, radius, cover, p, q, id)
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
              f'rate: {rate}')
        rates.append(rate)

    print(f'Average discovering rate: {sum(rates) / len(rates)}')


def main(args):
    # 参数获取
    num_nodes = args.num
    interval = args.inter
    angle_offset = args.angle_offset
    time_offset = args.time_offset
    scope = args.scope
    radius = args.radius
    cover = args.cover
    
    # 随机数分布
    P = [3, 5, 7, 11, 13]
    total_time = 11 * 13   # 应该根据质数分布计算

    # 节点生成
    nodes = create_ournodes(num_nodes, P, angle_offset, time_offset, scope, radius, cover)

    # 邻居初始化
    for node in nodes:
        node.find_neighbors(nodes)

    # 画布初始化
    fig = plt.figure(figsize=(10, 10))

    # 程序主体循环
    for i in range(total_time * 2):
        # 可视化
        visualize_network(nodes, fig)
        
        # 判断邻居关系
        for node in nodes:
            node.check_neighbors(i)

        # 更新节点朝向
        for node in nodes:
            node.update_orientation(i)
            
        # 休眠一段时间
        time.sleep(interval)
    
    # 统计邻居发现结果
    count(nodes)

    # cal_time

    # 根据节点分布情况换用更合适的P
    # TODO


def HDND(args):
    # 参数获取
    num_nodes = args.num
    interval = args.inter
    angle_offset = args.angle_offset
    time_offset = args.time_offset
    radius = args.radius
    cover = args.cover
    
    # 随机数分布
    P = [3, 5, 7, 11, 13]
    total_time = 11 * 13   # 应该根据质数分布计算

    # 节点生成
    nodes = create_hdndnodes(num_nodes, P, angle_offset, time_offset, radius, cover)

    # 邻居初始化
    for node in nodes:
        node.find_neighbors(nodes)

    # 画布初始化
    fig = plt.figure(figsize=(10, 10))

    # 程序主体循环
    for i in range(total_time * 2):
        # 可视化
        visualize_network(nodes, fig)
        
        # 判断邻居关系
        for node in nodes:
            node.check_neighbors(i, total_time)

        # 更新节点朝向
        for node in nodes:
            node.update_orientation(i, total_time)
            
        # 休眠一段时间
        time.sleep(interval)
    
    # 统计邻居发现结果
    count(nodes)
    

if __name__ == "__main__":
    args = utils.get_args()
    main(args)
    #HDND(args)
