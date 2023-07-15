from os import truncate
import numpy as np
import random


class Node:
    def __init__(self, x, y, scope, radius, cover, angle_offset, time_offset):
        self.x = x   # 节点x轴坐标
        self.y = y   # 节点y轴坐标
        self.scope = scope   # 节点漂浮范围半径
        self.radius = radius   # 通信半径
        self.cover = cover   # 收发范围扩散角度数
        self.angle_offset = angle_offset   # 正北方向的误差偏移量
        self.time_offset = time_offset   # 起始工作时间的偏移量
        self.orientation = 0   # 节点朝向
        self.status = 1   # 节点收（0）发（1）状态
        self.potential_neighbors = []   # 在通信范围内的强邻居
        self.discovered_neighbors = dict()   # 已经发现的邻居和次数


    def find_neighbors(self, nodes):
        for node in nodes:
            if node is not self:
                distance = np.sqrt((self.x - node.x) ** 2 + (self.y - node.y) ** 2)
                if distance + self.scope * 2 <= self.radius:
                    self.potential_neighbors.append(node)


    def calculate_angle(self, node):
        delta_x = node.x - self.x
        delta_y = node.y - self.y
        angle_rad = np.arctan2(delta_x, delta_y)
        angle_deg = np.degrees(angle_rad)
        return (angle_deg + 360) % 360


    def check_neighbor_orientation(self, node):
        if (abs(self.orientation - self.calculate_angle(node)) <= self.cover and
            abs(node.orientation - node.calculate_angle(self)) <= node.cover):
            return True
        else:
            return False


    def check_neighbor_status(self, node):
        return self.status == 0 and node.status == 1


    def check_neighbor_conflict(self, nodes):
        return len(nodes) <= 1


    def check_neighbors(self, cur_time):
        if cur_time < self.time_offset:
            return

        neighbors = []
        for neighbor in self.potential_neighbors:
            if (self.check_neighbor_conflict(neighbors) and
                self.check_neighbor_status(neighbor) and
                self.check_neighbor_orientation(neighbor)):
                neighbors.append(neighbor)

        if len(neighbors) == 1:
            if neighbors[0] not in self.discovered_neighbors:
                self.discovered_neighbors[neighbors[0]] = 0

            self.discovered_neighbors[neighbors[0]] += 1


    def count_neighbors(self):
        total = len(self.potential_neighbors)
        count = sum(1 for v in self.discovered_neighbors.values() if v >= 2)
        return count / total

    
    def get_divide_num(self):
        pass


    def change_status(self, cur_time):
        pass


    def update_orientation_status(self, cur_time):
        pass


class OurNode(Node):
    def __init__(self, x, y, scope=3, radius=15, cover=120, angle_offset=0, time_offset=0, p=3, P=[3, 5, 7]):
        super().__init__(x, y, scope, radius, cover, angle_offset, time_offset)
        self.p = p   # 划分质数
        self.P = P   # 质数分布
        self.orientation = ((180.0 / p) + self.angle_offset) % 360   # 初始朝向
        self.angle_increment = 360.0 / p   # 角度增量


    def get_divide_num(self):
        return self.p


    def change_status(self, cur_time):
        self.status = 1 if cur_time % self.p == 0 else 0
    
    
    def update_orientation_status(self, cur_time):
        if cur_time < self.time_offset:
            return

        # 2pq的值
        pq = 2 * self.P[-1] * self.P[-2]
        # 更新节点朝向
        if cur_time > 0 and cur_time % pq == 0:
            self.orientation = (self.orientation + self.angle_increment) % 360
        # 更新节点收发
        self.change_status(cur_time)
        # 经过(2pq)^2后重新分配p
        if cur_time > 0 and cur_time % (pq ** 2) == 0:
            self.reallocate_p()

            
    def reallocate_p(self):
        p = random.choice(self.P)
        self.p = p
        self.orientation = ((180.0 / p) + self.angle_offset) % 360
        self.angle_increment = 360.0 / p
        

class HDNDNode(Node):
    def __init__(self, x, y, scope=3, radius=15, cover=120, angle_offset=0, time_offset=0, p=3, q=5, id='101010'):
        super().__init__(x, y, scope, radius, cover, angle_offset, time_offset)
        self.p = p   # 接收状态的角速度
        self.q = q   # 发送状态的角速度
        self.s = id + '0' * (len(id) // 2 + 1) + '1' * ((len(id) + 1) // 2)   # 01状态序列
        self.count = 1   # 转动次数统计
        self.index = 0   # 状态序列下标
        self.orientation = (180.0 / p) % 360 if id[0] == '0' else (180.0 / q) % 360   # 初始朝向


    def get_divide_num(self):        
        return self.p if self.status == 0  else self.q
    

    def change_status(self, cur_time):
        self.index = (self.index + 1) % len(self.s)
        self.status = int(self.s[self.index]) - 0


    def update_orientation_status(self, cur_time):
        if  cur_time < self.time_offset:
            return
        
        n = self.get_divide_num()
        self.count += 1
        if self.count == 2 * n + 1:
            self.change_status(cur_time)
            n = self.get_divide_num()
            self.orientation = (180.0 / n) % 360
            self.count = 1
        else:
            increment = 360.0 / n
            self.orientation = (self.orientation + increment) % 360        
        

class RandomNode(Node):
    def __init__(self, x, y, scope, radius, cover, angle_offset, time_offset):
        super().__init__(x, y, scope, radius, cover, angle_offset, time_offset)
        self.orientation = random.randint(0, 360)

        
    def get_divide_num(self):
        return 0


    def change_status(self, cur_time):
        # 90%几率为发送状态
        self.status = 1 if random.randint(0, 100) > 10 else 0
    
    def update_orientation_status(self, cur_time):
        if cur_time < self.time_offset:
            return

        self.orientation = random.randint(0, 360)
        self.change_status(cur_time)
                            

class MLENode(Node):
    def __init__(self, x, y, scope, radius, cover, angle_offset, time_offset):
        super().__init__(x, y, scope, radius, cover, angle_offset, time_offset)
        self.p = int(360.0 / cover)   # 扇区划分
        self.orientation = cover / 2   # 初始朝向
        self.angle_increment = cover   # 角度增量
        self.weights = {i: 10.0 for i in range(self.p)}   # 选择各扇区的概率权重


    def get_divide_num(self):
        return self.p


    def change_status(self, cur_time):
        # 90%几率为发送状态
        self.status = 1 if random.randint(0, 100) > 10 else 0


    def update_orientation(self, cur_time):
        if cur_time < self.time_offset:
            return

        # 根据weights概率选择节点朝向
        keys = list(self.weights.keys())
        values = [value / sum(self.weights.values()) for value in self.weights.values()]
        selected_key = random.choices(keys, weights=values, k=1)[0]
        #print(self.weights)
        #print(selected_key)
        self.orientation = self.cover / 2 + (self.cover * selected_key)
        # 更新节点收发
        self.change_status(cur_time)


    def check_neighbors(self, cur_time):
        if cur_time < self.time_offset:
            return

        neighbors = []
        for neighbor in self.potential_neighbors:
            if (self.check_neighbor_conflict(neighbors) and
                self.check_neighbor_status(neighbor) and
                self.check_neighbor_orientation(neighbor)):
                neighbors.append(neighbor)

        if len(neighbors) == 0:
            # 如果此时此扇区未发现邻居 则该扇区权重-1
            self.weights[(self.orientation - self.cover/ 2) / self.cover] -= 1
            
        if len(neighbors) == 1:
            if neighbors[0] not in self.discovered_neighbors:
                self.discovered_neighbors[neighbors[0]] = 0

            self.discovered_neighbors[neighbors[0]] += 1
            # 如果此时此扇区成功发现邻居 则该扇区权重+1
            self.weights[(self.orientation - self.cover/ 2) / self.cover] += 1


if __name__ == "__main__":
    A = OurNode(0, 0)
    B = OurNode(-3, 4)
    
    delta_x = B.x - A.x
    delta_y = B.y - A.y
    angle_rad = np.arctan2(delta_x, delta_y)
    angle_deg = np.degrees(angle_rad)

    print((angle_deg + 360) % 360)
