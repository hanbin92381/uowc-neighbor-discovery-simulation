import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge


def visualize_network(nodes, fig):
    # 不同质数对应不同颜色
    colors = ['blue', 'green', 'grey', 'red', 'purple', 'pink', 'cyan', 'orange']
    
    # 获取当前图像对象
    ax = fig.gca()

    # 清空当前图像
    ax.cla()

    # 设置坐标轴范围
    plt.xlim(-10, 70)
    plt.ylim(-10, 70)

    # 绘制通信范围圆圈和分割线
    for node in nodes:
        # 获取划分个数
        n = node.get_divide_num()
        
        # 在节点位置绘制红色原点
        plt.plot(node.x, node.y, 'ro')
        
        # 绘制通信范围圆圈
        circle = Circle((node.x, node.y), node.radius, linewidth=1,edgecolor='gray', linestyle='dashed', fill=False, alpha=0.5)
        plt.gca().add_patch(circle)

        # 绘制分割线
        if n > 0:
            for i in range(n):
                angle = (i * (360.0 / n) + node.angle_offset) % 360
                line_x = [node.x, node.x + node.radius * np.sin(np.deg2rad(angle))]
                line_y = [node.y, node.y + node.radius * np.cos(np.deg2rad(angle))]
                plt.plot(line_x, line_y, linewidth=1, color='gray', linestyle='dashed', alpha=0.5)

        # 突出显示当前朝向所在的分区
        if n == 0: n = 360 / node.cover
        start_angle = 90 - node.orientation + (360 / (2 * n))
        end_angle = 90 - node.orientation - (360 / (2 * n))
        # 在 Wedge 函数中，角度参数是相对于正x轴方向的逆时针方向来定义的，而不是相对于正北方向
        wedge = Wedge((node.x, node.y), node.radius, end_angle, start_angle, facecolor=colors[int(3 * n) % len(colors)], alpha=0.3)
        plt.gca().add_patch(wedge)

    # 绘制节点位置和朝向
    for node in nodes:
        angle = np.deg2rad(node.orientation)
        dx = node.radius / 2 * np.sin(angle)  # 计算箭头在x轴上的位移
        dy = node.radius / 2 * np.cos(angle)  # 计算箭头在y轴上的位移
        plt.arrow(node.x, node.y, dx, dy, head_width=1, color='gray')

    # 显示图像并暂停一段时间
    plt.draw()
    #plt.show(block=False)
    plt.pause(0.1)  # 暂停时间可以根据需要进行调整
