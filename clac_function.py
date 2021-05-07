import numpy as np
from matplotlib.colors import Colormap
import matplotlib.pyplot as plt
from PIL import Image
from PyQt5.QtCore import QThread,pyqtSignal
import pandas as pd
from pprint import pprint

class CalcHologram(QThread):
    _sum = pyqtSignal(int)  # 信号类型 int

    def __init__(self,fname,iter_num):
        super(CalcHologram,self).__init__()
        self.fname = fname
        self.iter_num = iter_num
        self.tuple = None
    def run(self):
        for i in calcHologram_f(self.fname,self.iter_num):
            if isinstance(i,tuple):
                # return i
                self.tuple = i
                self._sum.emit(-1)
            else:
                self._sum.emit(i)
# 相位恢复算法,也就是GS算法
def recoveryHologram(fname):
    # 种下随机种子
    np.random.seed()
    image0 = Image.open(fname)
    # 转化成灰度图
    image0 = image0.convert('L')
    # 归一化
    image0 = np.abs(np.array(image0)) / np.max(np.abs(np.array(image0)))
    # copy一份
    image1 = np.array(image0)
    # 设置随机相位
    r,c = image1.shape
    randAngle = np.random.rand(r,c) * np.pi *2
    # 开始圏三
    image1 = image1*np.exp(1j*randAngle)
    # 开始圈四
    image2 = np.fft.ifft2(np.fft.fftshift(image1))
    for i in range(500):
        # 再次归一化
        angle = np.angle(image2)
        image = np.exp(1j*angle)
        image = np.fft.fftshift(np.fft.fft2(image))
        imgabs = np.abs(image)/np.max(np.abs(image))
        # 先将两个数组降维成一维
        sim = np.corrcoef(image0.flatten(),imgabs.flatten())
        # image0和imgabs的相关系数超过0.995满足条件跳出循环
        if sim[0,1] >= 0.995:
            break
        # 开始迭代
        else:
            angle = np.angle(image2)
            image2 = np.exp(1j*angle)
            image3 = np.fft.fftshift(np.fft.fft2(image2))
            # 增加负反馈调节
            imgabs = np.abs(image3) / np.max(np.abs(image3))
            angle  = np.angle(image3)
            image3 = np.exp(1j*angle)
            image3 = image0*image3

            image2 = np.fft.ifft2(np.fft.fftshift(image3))
    # 循环出来了之后，就是说明image2成功了
    # 但是这时的image2还是在傅里叶空间上的image2
    angle_f = np.angle(image2)
    image4 = np.fft.fftshift(np.fft.fft2(image2))
    imgabs = np.abs(image4)
    angle = np.angle(image4)
    return imgabs * np.exp(1j*angle)

# 首先整理一下思路，这个计算全息的关键就是将物光的相位提取出来，
# 而且这个提取出来的相位还要满足，用激光去照射在这个全息图上的时候，
# 还都要满足能够把原来的图片还原出来
def CalcHologram(fname):
    # 返回出来的是带有相位信息的物光复函数
    f = recoveryHologram(fname)
    imgabs = np.abs(f)
    plt.imshow(imgabs,cmap=plt.cm.gray)
    plt.show()
    # 抽样的步骤已经完成了
    # image0 = Image.open(fname)
    # ax1 = plt.subplot(221)
    # ax1.imshow(image0)
    # temp = np.array(image0)
    # image0 = image0.convert('L')
    # image0 = np.abs(np.array(image0)) / np.max(np.abs( np.array(image0)))
    # ax2 = plt.subplot(222)
    # 原来之前不是没有作对只是显示方式的问题
    # ax2.imshow(image0,cmap=plt.cm.gray)
    # plt.title('gray photo')

if __name__ =="__main__":
    CalcHologram('./res/test.jpg')