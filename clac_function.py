import numpy as np
from PIL import Image
# 计算相位图,使用PIL模块和np模块配合使用
def calcHologram_f(fname,iter_num):
    np.random.rand()
    # 抽样
    I = Image.open(fname)
    L = I.convert('L')
    image0 = np.array(L)
    image0 = image0/np.max(image0)
    # 随机相位图
    imgangle = np.random.random(image0.shape)
    image1 = np.exp(1j*imgangle)

    # 先进行频谱搬移，在作傅里叶逆变换
    image2 = np.fft.ifft2(np.fft.fftshift(image1))
    for i in range(iter_num):
        # 迭代判据
        # imgabs = np.abs(image2)
        imgangle = np.angle(image2)
        image = np.exp(1j*imgangle)
        imgabs = np.abs(image)
        sim = np.corrcoef(image0,imgabs)
        # print(imgabs[imgabs == 1])
        
        if sim[1,2] >= 0.995:
            # 满足判断条件了
            break

        else:
            # 开始迭代
            # 单位振幅，这里生成的是位像图，所以就不关心振幅
            imgangle = np.angle(image2)
            image2 = np.exp(1j*imgangle)
            yield i
            # 取

