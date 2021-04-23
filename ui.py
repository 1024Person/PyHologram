# 纯代码实现UI界面
import sys
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QDoubleSpinBox
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from clac_function import *
from PyQt5.QtWidgets import QProgressBar


class UI(QWidget):
    def __init__(self):
        super(UI, self).__init__()
        # 初始化变量
        self.initVar()
        # 初始化界面UI
        self.initUI()
        # 为每一个控件绑定信号和槽函数
        self.initConnect()

    def initVar(self):
        self.iter_num = 500  # 迭代次数
        self.currentfname = 0
        self.subject_pixmap = 0

    def initUI(self):

        # centeralWidget = QWidget(self)
        self.totalGroup = QGroupBox('计算全息图', self)
        self.show_subject_label = QLabel('物', self)
        self.show_xiang_label = QLabel('像', self)
        self.show_xiang_label.setAlignment(Qt.AlignCenter)
        self.show_subject_label.setAlignment(Qt.AlignCenter)
        self.load_subject_btn = QPushButton('导入“物”', self)
        self.clac_xiang_btn = QPushButton('计算全息图', self)
        self.show_subject_label.setFrameShape(QtWidgets.QFrame.Box)
        self.show_subject_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.show_xiang_label.setFrameShape(QtWidgets.QFrame.Box)
        self.show_xiang_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        # 显示像和计算像以及按钮的布局
        gridlayout = QGridLayout()
        gridlayout.addWidget(self.show_xiang_label, 0, 1)
        gridlayout.addWidget(self.show_subject_label, 0, 0)
        gridlayout.addWidget(self.clac_xiang_btn, 1, 1)
        gridlayout.addWidget(self.load_subject_btn, 1, 0)
        gridlayout.setSpacing(10)
        self.totalGroup.setLayout(gridlayout)
        # ---------------------------------------
        self.input_group = QGroupBox('设置细节')
        self.label_show = QLabel('计算进度：')
        self.progress_bar = QProgressBar(self)  # 显示当前的迭代进度
        self.progress_bar.setMaximum(self.iter_num - 1)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setToolTip("计算进度：")
        self.progress_bar.setMaximumWidth(self.label_show.width())
        # self.progress_bar.De
        self.save_btn = QPushButton('保存', self)
        self.theta_label = QLabel('衍射角(度)：')
        self.distance_label = QLabel('衍射距离(m)：')

        self.theta_spinbox = QDoubleSpinBox(self)
        self.distance_spinbox = QDoubleSpinBox(self)
        self.distance_spinbox.value = 0
        self.theta_spinbox.value = 0

        self.theta_spinbox.setSingleStep(0.1)
        self.theta_spinbox.setDecimals(1)
        self.distance_spinbox.setSingleStep(0.1)
        self.distance_spinbox.setDecimals(1)

        # 衍射角和衍射距离的布局

        input_gridlayout = QGridLayout()
        input_gridlayout.addWidget(self.theta_label, 0, 0)
        input_gridlayout.addWidget(self.theta_spinbox, 0, 1)
        input_gridlayout.addWidget(self.distance_label, 1, 0)
        input_gridlayout.addWidget(self.distance_spinbox, 1, 1)
        input_gridlayout.addWidget(self.save_btn, 1, 3)
        input_gridlayout.addWidget(self.progress_bar, 0, 3)
        input_gridlayout.addWidget(self.label_show, 0, 2)
        input_gridlayout.setSpacing(5)
        self.input_group.setLayout(input_gridlayout)  # 为这个空间组添加布局
        # -------------------------------------
        # 总布局
        self.total_layout = QGridLayout()
        # self.total_layout.addWidget(self.save_btn, 2, 1)
        # self.total_layout.addWidget(self.progress_bar,1,1)
        self.total_layout.addWidget(self.input_group, 1, 0)
        self.total_layout.addWidget(self.totalGroup, 0, 0, 1, 2)
        self.setLayout(self.total_layout)
        # centeralWidget.setLayout(total_layout)
        # self.setCentralWidget(centeralWidget)
        self.setWindowIcon(QIcon('./res/icon.png'))
        self.setWindowTitle('GS算法计算光学全息图')
        self.setGeometry(300, 300, 800, 700)

    def initConnect(self):
        # 导入图片的绑定
        self.load_subject_btn.clicked.connect(self.loadSubject)
        # 保存图片的绑定
        # 计算全息图的绑定
        self.clac_xiang_btn.clicked.connect(self.clacHologram)

        self.save_btn.clicked.connect(self.saveHologram)

    # 更新ProgressBar和按钮
    def updateProBar(self, r):
        if r != -1:
            self.progress_bar.setValue(r)
        else:
            self.load_subject_btn.setEnabled(True)
            self.clac_xiang_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
            self.clac_xiang_btn.setText('计算全息图')
            hologram, imgabs = Image.fromarray(((self.calc_thread.tuple[0] + np.pi) / (np.pi * 2))), \
                               Image.fromarray(self.calc_thread.tuple[1] * 255)
            hologram = hologram.convert('L')
            imgabs = imgabs.convert('L')
            hologram.save('hologram.jpg')
            imgabs.save('imgabs.jpg')

    def close(self):
        self.calc_thread.quit()
        sys.exit(0)

    def clacHologram(self):
        # 计算全息图
        if self.currentfname:
            self.progress_bar.setValue(0)
            self.clac_xiang_btn.setText('计算中...')
            self.save_btn.setEnabled(False)
            self.clac_xiang_btn.setEnabled(False)  # 设置成不可以点击的
            self.load_subject_btn.setEnabled(False)
            # 创建一个线程,这里要加上self，这是一个坑，如果不加上self,出了这个函数，这个线程就会被销毁
            self.calc_thread = CalcHologram(self.currentfname, self.iter_num)
            self.calc_thread._sum.connect(self.updateProBar)  # 将线程发送过来的信号直接挂载到槽函数上去
            self.calc_thread.start()
        # calcHologram(self.current_fname)

    def saveHologram(self):
        # 保存全息图
        QFileDialog().getSaveFileName(directory='/home', filter='png格式(*.png);;jpg格式(*.jpg);;bmp格式(*.bmp)')

    def loadSubject(self):
        # 调用这个方法，返回的是文件路径和文件类型
        file_fliter = ".png(*.png);;.jpg(*.jpg);;.bmp(*.bmp)"
        fname, ftype = QFileDialog.getOpenFileName(self, '选择“物”', '/home', file_fliter)
        # self.show_subject_label.setPixmap(QPixmap(fname))
        # self.show_subject_label.setScaledContents(False)
        if fname:
            self.show_subject_label.clear()
            self.currentfname = fname  # 将文件名字保存下来
            # self. = QPixmap(fname)  # 虽然label上面显示不了，但是需要保存原始数据才可以进行运算
            # subject_show_pixmap = self.subject_pixmap.scaled(self.show_subject_label.width(),self.show_subject_label.height())
            self.subject_pixmap = QPixmap(fname)
            subject_show_pixmap = self.subject_pixmap.scaled(self.show_subject_label.width(),
                                                             self.show_subject_label.height())
            self.show_subject_label.setPixmap(subject_show_pixmap)
            # 感觉这个方法不是很好
            # self.scalePixmap()

    def scalePixmap(self):
        # 设置一个图片的缩放方法,不改变图片原有的尺寸
        if self.subject_pixmap.height() > self.show_subject_label.height() or \
                self.subject_pixmap.width() > self.show_subject_label.width():
            h_ = self.subject_pixmap.height() / self.show_subject_label.height()  # 计算加载的图片的高度是label的多少倍
            w_ = self.subject_pixmap.width() / self.show_subject_label.width()  # 计算加载的图片的宽度是label的多少倍
            if w_ > 1:
                w = round(self.subject_pixmap.width() / w_)
                if h_ > 1:
                    h = round(self.subject_pixmap.height() * (w / self.subject_pixmap.width()))
                else:
                    # 如果height并没有比label的高，就加上一个0.5
                    h = round(self.subject_pixmap.height() * (w / self.subject_pixmap.width() + 0.5))
            elif w_ <= 1:
                if h_ > 1:
                    h = round(self.subject_pixmap.height() / h_)
                    w = round(self.subject_pixmap.width() * (h / self.subject_pixmap.height() + 0.5))
                else:
                    # 如果图片本身就比label小的话，就不需要处理了吧
                    h = self.subject_pixmap.height()
                    w = self.subject_pixmap.width()
            show_subject_pixmap = self.subject_pixmap.scaled(w, h)
            self.show_subject_label.setPixmap(show_subject_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = UI()
    ex.show()
    sys.exit(app.exec_())
