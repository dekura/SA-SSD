'''
@Author: Guojin Chen
@Date: 2020-06-20 14:30:27
LastEditTime: 2021-01-07 14:30:37
@Contact: cgjhaha@qq.com
@Description: draw vels
'''
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Draw multiple points.
def draw_velodyne(velsets):
    # velsets[:, 0] = velsets[:, 0]/100
    # velsets[:, 1] = velsets[:, 1]/100
    # x axis value list.
    x_number_list = velsets[:,0]
    # y axis value list.
    y_number_list = velsets[:,1]
    # Draw point based on above x, y axis values.
    plt.scatter(x_number_list, y_number_list, marker='o', s=0.01, c='#722C72')
    # Set chart title.
    plt.title("Bird eye view of velodyne")
    # Set x, y label text.
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig('./gds2vel_bev.png', dpi=500)
    plt.show()

# if __name__ == '__main__':
    # draw_multiple_points()
def draw_velodyne_3d(velsets):
    x = velsets[:,0]
    y = velsets[:,1]
    z = velsets[:,2]
    for i in [1]:
        x = np.concatenate((x,x))
        y = np.concatenate((y,y))
        # print('x:',x.shape)
    # print('z', z.shape)
    z1 = np.zeros(z.shape)
    z1[:] = 0.4
    z = np.concatenate((z, z1))
    # print('z', z.shape)
    # z2 = np.zeros(z.shape)
    # z2[:] = 0.3
    # z = np.concatenate((z, z2))
    # print('z', z.shape)
    # z3 = np.zeros(z.shape)
    # z3[:] = 0.4
    # z = np.concatenate((z, z3))
    # print('z', z.shape)
    # z = np.concatenate(z, z1, z2, z3)

    # data = np.arange(24).reshape((8, 3))
    # print(data)
    # x = data[:, 0]  # [ 0  3  6  9 12 15 18 21]
    # y = data[:, 1]  # [ 1  4  7 10 13 16 19 22]
    # z = data[:, 2]  # [ 2  5  8 11 14 17 20 23]
    fig = plt.figure()
    # ax = Axes3D(fig)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, s=0.01, marker=',', c='#722C72')
    # 添加坐标轴(顺序是Z, Y, X)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.savefig('./gds2vel_3d.png', dpi=500)
    plt.show()