from threading import Thread
import NDIlib as ndi
import cv2 as cv
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt6.QtWidgets import QInputDialog
from PyQt6 import QtCore
from PyQt6.QtWidgets import  QWidget, QLabel, QVBoxLayout, QPushButton,  QHBoxLayout
from ndiReceiverClass import NDI_Receiver
from utils import findNDIsources

# ----------- GLOBAL VALUES -----------------------

MARGIN_VALUE = 30  # 60
NDI_TITLE_HEIGHT = 50
SCREEN_BORDER = 40
COUNTER = 0
X_FACTOR = 0
Y_FACTOR = 0

# ---------------------------------------------------------

class SingleWindow(QWidget):
    def __init__(self, title, width, height, xPos, yPos, divisor):
        super().__init__()
        self.winHeight = int(height)
        self.winWidth = int(width) - int(NDI_TITLE_HEIGHT / int(divisor))
        self.winXPos = int(xPos) + X_FACTOR
        self.winYPos = int(yPos) + Y_FACTOR
        self.divisor = int(divisor)
        self.setWindowTitle(title)
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint)# | QtCore.Qt.WindowType.FramelessWindowHint)
        self.setGeometry(100, 100, int(width), int(height))

        self.move(int(xPos), int(yPos))

        self.currentSourceName = 'SmallWindow'
        self.ndiNameString = 'SMALL_WINDOW'
        self.ndiReceiver = NDI_Receiver()
        self.alreadyOpenStreamFlag = 0  # this flag is meant to indicate whether ndi reciver.connect(ndi_source)
        self.playFlag = 0  # this flg is to control PLAY and PAUSE function

        self.nameStr = ''
        self.playStreamFlag = 0

        self.layout = QVBoxLayout()
        self.hLayout = QHBoxLayout()
        self.label = QLabel(title)
        self.label.setStyleSheet("font-size: 24pt;background-color : light-blue; border: 2px solid black;")
        self.label.setGeometry(self.winXPos, self.winYPos, self.winWidth, self.winHeight)

        self.titleTextField = QLabel("SOURCE-NAME")  # QPushButton("SINGLE-WINDOW")
        self.titleTextField.setEnabled(False)
        self.titleTextField.setStyleSheet("font-size: 14pt; color: red; text-align: center; font-weight: bold; font-family:\
                                              'Arial';  border: 2px solid black; border-radius: 5px; background_color = lightblue; ")
        self.titleTextField.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(self.winXPos, self.winYPos, self.winWidth, int(NDI_TITLE_HEIGHT / self.divisor))
        self.buttonNewStream = QPushButton("New NDI Stream")

        self.buttonPlayVideo = QPushButton("PLAY/PAUSE")
        self.buttonPlayVideo.setEnabled(False)

        self.audioStatusCheckBox = QLabel("AUDIO-STATUS")
        self.audioStatusCheckBox.setEnabled(True)
        self.audioStatusCheckBox.setContentsMargins(1, 1, 1, 1)
        self.audioStatusCheckBox.setStyleSheet("background-color : white; ")

        self.buttonEXIT = QPushButton("EXIT")

        self.buttonNewStream.clicked.connect(self.launch_new_window)
        self.buttonPlayVideo.clicked.connect(self.play_video)
        self.buttonEXIT.clicked.connect(self.exit_instance)

        self.hLayout.addWidget(self.buttonNewStream)
        self.hLayout.addWidget(self.buttonPlayVideo)
        self.hLayout.addWidget(self.audioStatusCheckBox)
        self.hLayout.addWidget(self.buttonEXIT)

        self.layout.addWidget(self.titleTextField)
        self.layout.addWidget(self.label)
        # self.layout.addStretch()
        self.layout.addLayout(self.hLayout)

        self.setLayout(self.layout)
        self.show()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.blue, 4))
        painter.drawRect(self.rect())

    def play_video(self):
        if self.playFlag == True:
            self.playStreamFlag = 0
            self.buttonPlayVideo.setText("PLAY")
        else:
            self.pause_video()

    def pause_video(self):
        #self.playFlag = True
        self.playStreamFlag = 1
        self.buttonPlayVideo.setText("PAUSE")

    def exit_instance(self):
        exit(0)

    def launch_new_window(self):
        # print("SMALL_WINDOW Barkaat, ready to launch a new stream")
        self.audioStatusCheckBox.setStyleSheet("background-color : white; ")
        self.buttonPlayVideo.setEnabled(False)
        items = list()
        sources = findNDIsources()
        for i, s in enumerate(sources):
            items.insert(i, s.ndi_name)
            # print('names of the ndi source is = ', s.ndi_name)

        dlg = QInputDialog(self)
        dlg.resize(800, 100)
        selectNDIstream, ok = dlg.getItem(dlg, "NDI-Stream ", "list of NDI Streams available", items, 0, False)

        if not ok:  # and self.alreadyOpenStreamFlag == 0:
            print("SMALL_WINDOW no stream selected at the initial start")
            return

        elif ok:
            print("\n SMALL_WINDOW the selected stream is ", selectNDIstream)
            if self.ndiNameString == selectNDIstream:
                print("SMALL_WINDOW inside launch_new_window slected and running streams are identical. RETURN ")
                return

            else:
                print("SMALL_WINDOW inside launch_new_window function OK was pressed at the dialog box ")
                i = 0;
                j = 0;
                tempStr = " "
                for s in (items):
                    if selectNDIstream == s:
                        self.ndiNameString = s
                        j = i
                        break
                    i = i + 1

                print("SMALL_WINDOW inside launch_new_window selected and running streams are different. PROCEED ",
                      sources[j])

                try:
                    if self.alreadyOpenStreamFlag == 1:
                        print('one stream is already running in SMALL_WINDOW, we change to the next one',
                              self.ndiNameString.upper())
                        self.currentSourceName = sources[j]
                        # self.setWindowTitle(s)
                        self.titleTextField.setText(self.ndiNameString.upper())
                        self.ndiReceiver.attachSource(sources[j])
                        self.buttonPlayVideo.setEnabled(True)
                        self.buttonPlayVideo.setText("PLAY")
                        self.buttonPlayVideo.setStyleSheet("background-color : green; ")
                        self.playFlag = 1
                        return

                    else:
                        print('SMALL_WINDOW, we play a new stream the 1st time now', self.ndiNameString.upper())

                        self.currentSourceName = sources[j]
                        self.titleTextField.setText(self.ndiNameString.upper())
                        self.thread = Thread(target=self.pyNDIPlayer, name='SMALL_NDI',
                                             args=(self.ndiNameString, sources[j], \
                                                   self.winWidth, self.winHeight, self.winXPos,
                                                   self.winYPos))
                        self.buttonPlayVideo.setEnabled(True)
                        self.buttonPlayVideo.setText("PLAY")
                        self.buttonPlayVideo.setStyleSheet("background-color : green; ")
                        self.playFlag = 1
                        self.thread.run()

                except Exception as e:
                    print("SMALL_WINDOW process did not launch successfullty", e.args[0])


    # --------------------------------------------------------------------------------------------------------------

    def pyNDIPlayer(self, nameStr, source, width, height, xPos, yPos):

        reducedWidth = width - 2 * SCREEN_BORDER
        reducedHeight = height - int((NDI_TITLE_HEIGHT + MARGIN_VALUE) / self.divisor)

        self.setWindowTitle(nameStr)

        if self.playStreamFlag == 0:
            self.playStreamFlag = 1

        if self.alreadyOpenStreamFlag == 0:
            self.alreadyOpenStreamFlag = 1
        if self.playFlag == 0:
            self.playFlag = 1

        self.buttonPlayVideo.setEnabled(True)
        self.buttonPlayVideo.setText("PAUSE")
        self.buttonPlayVideo.setStyleSheet("background-color: green;")

        print("inside the pyNDIPlayer 0")

        if not ndi.initialize():
            ndi.initialize()
            print("ndi.initialize():")

        self.ndiReceiver.attachSource(source)
        self.buttonPlayVideo.setEnabled(True)
        self.buttonPlayVideo.setStyleSheet("background-color: green;")

        #'''
        try:
            self.hide()
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
            self.show()
        except Exception as e:
            print('the window style did not change =  ', e.args[0])
                #'''

        for i in range(100):
            t, v, a, m = ndi.recv_capture_v2(self.ndiReceiver.receiver, 50)
            if a.no_samples == 0:
                sampleRate = a.sample_rate
                blockSize = a.no_samples
                totalChannels = a.no_channels
                ndi.recv_free_video_v2(self.ndiReceiver.receiver, v)
                ndi.recv_free_audio_v2(self.ndiReceiver.receiver, a)
                break

        print("about to enter the infinite while loop")

        while True:

            t, v, a, m = ndi.recv_capture_v2(self.ndiReceiver.receiver, 50)

            if t == ndi.FRAME_TYPE_VIDEO and self.playStreamFlag == 1:
                yuv_image = (v.data)
                img_height, img_width = v.yres, v.xres
                yuv_image_np = np.frombuffer(yuv_image, dtype=np.uint8)
                yuv_image_np_matrix = yuv_image_np.reshape((img_width, img_height, 4))
                rgb_image_np = cv.cvtColor(yuv_image_np_matrix, cv.COLOR_RGBA2BGR)
                rgb_image_qt = QImage(rgb_image_np.data, img_width, img_height, QImage.Format.Format_RGB888)
                img_resize = rgb_image_qt.scaled(reducedWidth, reducedHeight)
                self.label.setPixmap(QPixmap.fromImage(img_resize))
                cv.waitKey(1)
                ndi.recv_free_video_v2(self.ndiReceiver.receiver, v)
                self.playFlag = True
                continue
            elif t == ndi.FRAME_TYPE_VIDEO and self.playStreamFlag == 0:
                # self.label.setText("P A U S E D")
                self.label.setPixmap(QPixmap.fromImage(img_resize))
                cv.waitKey(1)
                ndi.recv_free_video_v2(self.ndiReceiver.receiver, v)
                self.playFlag = False
                continue

        print("pyNDIPlayer finished")

    # ______________________________________________________________________________________________________________________

