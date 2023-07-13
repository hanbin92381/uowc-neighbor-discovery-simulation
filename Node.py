import numpy as np


class Node:
    def __init__(self, x, y, scope, radius, cover):
        self.x = x   # 节点x轴坐标
        self.y = y   # 节点y轴坐标
        self.scope = scope   # 节点漂浮范围半径
        self.radius = radius   # 通信半径
        self.cover = cover   # 收发范围扩散角度数
        self.orientation = 0   # 节点朝向
        self.potential_neighbors = []   # 在通信范围内的强邻居
        self.discovered_neighbors = set()   # 已经发现的邻居


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


class OurNode(Node):
    def __init__(self, x, y, scope=3, radius=15, cover=120, p=3, angle_offset=0, time_offset=0):
        super().__init__(x, y, scope, radius, cover)
        self.p = p   # 划分质数
        self.angle_offset = angle_offset   # 正北方向的误差偏移量
        self.time_offset = time_offset   # 起始工作时间的偏移量
        self.orientation = ((180.0 / p) + self.angle_offset) % 360   # 初始朝向
        self.angle_increment = 360.0 / p   # 角度增量

        
    def update_orientation(self, cur_time):
        if cur_time < self.time_offset:
            return
        
        self.orientation = (self.orientation + self.angle_increment) % 360


    def check_neighbors(self, cur_time):
        if cur_time < self.time_offset:
            return
        
        for neighbor in self.potential_neighbors:
            if (abs(self.orientation - self.calculate_angle(neighbor))
                <= self.cover):
                if (abs(neighbor.orientation - neighbor.calculate_angle(self))
                    <= neighbor.cover):
                    self.discovered_neighbors.add(neighbor)
                    neighbor.discovered_neighbors.add(self)


class HDNDNode(Node):
    def __init__(self, x, y, scope=3, radius=15, cover=120, p=3, q=5, id='101010'):
        super().__init__(x, y, scope, radius, cover)
        self.p = p   # 接受状态的角速度
        self.q = q   # 发送状态的角速度
        self.s = id + '0' * (len(id) // 2 + 1) + '1' * ((len(id) + 1) // 2)   # 01指令序列
        self.orientation = 0
        self.angle_increment_p = 360.0 / p
        self.angle_increment_q = 360.0 / q


    def get_status(self, cur_time):
        return self.s[cur_time % len(self.s)]

    def update_orientation(self, cur_time):
        if self.get_status(cur_time) == '1':
            temp = self.angle_increment_q
        else:
            temp = self.angle_increment_p
        
        self.orientation = (self.orientation + temp) % 360


    def check_neighbors(self, cur_time):
        if self.get_status(cur_time) == '0':
            return
        
        for neighbor in self.potential_neighbors:
            if neighbor.get_status(cur_time) == '1':
                continue
            
            if (abs(self.orientation - self.calculate_angle(neighbor))
                <= self.cover):
                if (abs(neighbor.orientation - neighbor.calculate_angle(self))
                    <= neighbor.cover): 
                    self.discovered_neighbors.add(neighbor)
        
        
    
if __name__ == "__main__":
    A = OurNode(0, 0)
    B = OurNode(-3, 4)
    
    delta_x = B.x - A.x
    delta_y = B.y - A.y
    angle_rad = np.arctan2(delta_x, delta_y)
    angle_deg = np.degrees(angle_rad)

    print((angle_deg + 360) % 360)
