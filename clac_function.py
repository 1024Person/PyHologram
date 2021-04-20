import numpy as np
from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal


class CalcHologram(QThread):
    _sum = pyqtSignal(int)  # 信号类型 int

    def __init__(self, fname, iter_num):
        super(CalcHologram, self).__init__()
        self.fname = fname
        self.iter_num = iter_num
        self.tuple = None

    def run(self):
        for i in calcHologram_f(self.fname, self.iter_num):
            if isinstance(i, tuple):
                # return i
                self.tuple = i
                self._sum.emit(-1)  # 发出信号-1代表已经完成工作了
            else:
                self._sum.emit(i)


# 计算相位图,使用PIL模块和np模块配合使用
def calcHologram_f(fname, iter_num):
    # 抽样
    I = Image.open(fname)
    L = I.convert('L')
    image0 = np.array(L)

    image0 = np.abs(image0) / np.max(np.abs(image0))
    image1 = image0
    # 随机相位图
    imgangle = np.pi * 2 * np.random.random(image0.shape)
    image1 = image1 * np.exp(1j * imgangle)

    # 先进行频谱搬移，在作傅里叶逆变换
    image2 = np.fft.ifft2(np.fft.fftshift(image1))
    for i in range(iter_num):
        # 迭代判据
        # imgabs = np.abs(image2)
        imgangle = np.angle(image2)
        image = np.exp(1j * imgangle)
        image = np.fft.fftshift(np.fft.fft2(image))  # 还原到空域
        # 振幅归一化
        imgabs = np.abs(image) / np.max(np.abs(image))
        rmse = np.mean((imgabs - np.abs(image0)) ** 2) ** 0.5
        if rmse < 0.005:
            # 满足判断条件了
            print('出去了')
            break
        else:
            # 开始迭代
            # 单位振幅，这里生成的是位像图，所以就不关心振幅
            imgangle = np.angle(image2)
            image2 = np.exp(1j * imgangle)
            # print(i)
            yield i
            # 做一次傅里叶正变换
            image3 = np.fft.fftshift(np.fft.fft2(image2))
            # 取相位，设置负反馈
            imgangle = np.angle(image3)
            image3 = np.exp(1j * imgangle)
            image3 = image3 * (image0 + np.random.rand(1) * (image0 - imgabs))

            # 再次进行傅里叶正变换得到image2
            image2 = np.fft.ifft2(np.fft.ifftshift(image3))
    print("迭代结束")
    imgangle = np.angle(image2)

    # 在将image4做一次变换得到空域上的图片
    image4 = np.exp(1j * imgangle)
    image4 = np.fft.fftshift(np.fft.fft2(image4))
    imgabs = np.abs(image4) / np.max(np.abs(image4))
    imgangle = (imgangle + np.pi) / (2 * np.pi)

    yield (imgangle, imgabs)
