import matplotlib.pyplot as plt

# 给定的四个列表
x = [10, 20, 30, 40, 50]
# y1 = [186, 776, 1758, 2124, 5059]
# y2 = [688, 3967, 5808, 8505, 9308]
# y3 = [5566, 7287, 6472, 8971, 8012]
# y4 = [9037, 10278, 11573, 10525, 11925]

y1 = [123.9, 312.85, 602.1, 592.4, 1011.34]
y2 = [333.3, 1182.25, 2202.43, 1612.1, 2080.96]
y3 = [2771, 2562.25, 2624.03, 2433.13, 2503.88]
y4 = [4469.1, 4437.45, 5737.1, 4350.78, 5264.34]

# 创建折线图
plt.plot(x, y1, label='our')
plt.plot(x, y2, label='icdcs')
plt.plot(x, y3, label='iot')
plt.plot(x, y4, label='random')

# 添加标题和图例
plt.title('Line Chart')
plt.legend()

# 显示图形
plt.show()
plt.savefig('figures/fig2.png')
