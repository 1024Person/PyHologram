# 从网上终于看到了一种自己能看懂的python实现了T_T
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 计算全息图
# 参数：fname 文件路径
# 参数: L 图片的尺寸（或者说是记录平面的尺寸）
def calcHologram(fname,M,N):
    # 打开图片就是已经抽样结束了
    # image0 = Image.open(fname)
    S = M*N  # 抽样点数 
    # 每一行的像素点数是M，那么将所有的像素点除以每一行的像素点数结果就是有多少行
    row = np.linspace(0,S,M)
    columns = np.linspace(0,S,N)
    u,v = np.meshgrid(row,columns)
    lam = 6.328e-4    # 波长单位mm
    k = 2*np.pi / lam # 波数
    beta = 6   # 倾斜角
    b = k*np.sin(beta * np.pi / 180)   # 参考光的空间频率

    # 计算参考光
    Ruv = np.exp(1j*b*u)
    # 计算参考光的共轭光
    CRuv = np.conj(Ruv)

    Original = Image.open(fname)
    # 读取到的信息中包含红蓝绿三种颜色的强度，要转换成灰度图
    # 0~255
    Oxy_data = np.array(Original)
    r,g,b =Oxy_data[:,:,0], Oxy_data[:,:,1],Oxy_data[:,:,2]  # 读取三种颜色的数据
    Oxy = (r+g+b) / 3  # 光照强度信息
    # 计算出傅里叶空间中的物光复振幅分布
    Ouv = np.fft.fftshift(np.fft.fft2(Oxy))
    # 计算全息图
    Huv = Ruv + Ouv
    # H记录的是物光波Oxy的傅里叶变换谱Ouv
    # H就是傅里叶变换全息图
    H = Huv * np.conj(Huv)
    H = (H.astype(np.float))

    T = Ruv * H
    T = T.astype(np.float)
    R = np.fft.fftshift(np.fft.fft2(T))
    R = R.astype(np.float)


    # H是频域上的函数需要转换到空域上来
    # show_H = abs(np.fft.fft2(np.fft.fftshift(H)))
    plt.figure(1)
    plt.subplot(311)
    plt.imshow(H,'gray')
    plt.title("H")
    plt.subplot(312)
    plt.imshow(T)
    plt.title('T')
    plt.subplot(313)
    plt.imshow(R)
    plt.title('R')
    plt.show()
    



if __name__ == "__main__":
    W = 487
    H = 302
    calcHologram("./res/python.png",W,H)