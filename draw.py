import matplotlib.pyplot as plt

# 总时间
x = [10, 20, 30, 40, 50]
#y1 = [261, 735, 1301, 3676, 4570]
#y2 = [1878, 3447, 7552, 8387, 8430]
#y3 = [3489, 4181, 8706, 9459, 10618]
#y4 = [8374, 9739, 10083, 11554, 12525]
#y5 = [192, 310, 339, 388, 471]

y1 = [175.6, 334.35, 417.8, 685.6, 981.8]
y2 = [934.3, 1619.4, 1409.2, 1320.2, 1713.5]
y3 = [1854.1, 2352.3, 3009.8, 2645.4, 2934.9]
y4 = [4331.7, 4859.1, 4742.3, 5214.1, 4451.12]
y5 = [149.5, 193.9, 159.9, 191.5, 184.8]

# 创建折线图
plt.plot(x, y1, label='our')
plt.plot(x, y2, label='icdcs')
plt.plot(x, y3, label='iot')
plt.plot(x, y4, label='random')
plt.plot(x, y5, label='period')

# 添加标题和图例
#plt.title('Total time')
plt.title('Average time')
plt.legend()

# 显示图形
# plt.show()
#plt.savefig('figures/fig1.png')
plt.savefig('figures/fig2.png')
