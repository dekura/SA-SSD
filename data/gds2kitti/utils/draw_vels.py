'''
@Author: Guojin Chen
@Date: 2020-06-20 14:30:27
@LastEditTime: 2020-06-20 15:13:07
@Contact: cgjhaha@qq.com
@Description: draw vels
'''
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# Draw multiple points.
def draw_velodyne(velsets):
    # x axis value list.
    x_number_list = velsets[:,0]
    # y axis value list.
    y_number_list = velsets[:,1]
    # Draw point based on above x, y axis values.
    plt.scatter(x_number_list, y_number_list, s=0.01, c='black')
    # Set chart title.
    plt.title("visualize velodyne")
    # Set x, y label text.
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

# if __name__ == '__main__':
    # draw_multiple_points()
