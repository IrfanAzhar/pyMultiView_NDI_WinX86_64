import os
import ctypes
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6 import QtCore
import multiprocessing
from gen_window_function import run_generic_window
from single_window_function import run_single_window

# ----------- GLOBAL VALUES -----------------------

ORIG_X_POS = 0
ORIG_Y_POS = 0
HEIGHT_FACTOR = 100  # this value is introdcued to keep space for the bottom buttons of the main window to be visible all the time
SCREEN_WIDTH = 1920  # this is default value and it may get changed
SCREEN_HEIGHT = 1080 # this is default value and it may get changed
BUTTON_COLOR = QColor("#FF0000") #("(0, 120, 120)")   #('green')

X_FACTOR = 10
Y_FACTOR = 10

COUNTER = 0

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PY-MULTI-VIEW")
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnBottomHint | QtCore.Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("border: 2px solid black; border-radius: 5px; background_color = rgb(250, 250, 120); ")
        self.move(50, 10)

        self.winWidth = 450
        self.winHeight = 250
        self.divisor = 1


        self.layout = QVBoxLayout()
        self.vLayout = QVBoxLayout()
        self.hLayout = QHBoxLayout()

        self.label = QLabel(" ===================  LAUNCH NEW WINDOWS   =================== ")
        self.label.setStyleSheet("font-size: 24pt; color: red; text-align: center; font-weight: bold; font-family:\
                                              'Arial';  border: 2px solid black; border-radius: 5px; background_color = rgb(250, 250, 120); ")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.multipleFactor = '4by3'
        self.small_window_processes = []
        self.count = 0

        self.buttonMultipleWindow2by2 = QPushButton("2-by-2-WINS")
        self.buttonMultipleWindow2by2.setEnabled(True)
        self.buttonMultipleWindow2by2.setStyleSheet("background-color: rgb(255, 250, 120);")
        self.buttonMultipleWindow2by2.clicked.connect(self.launch_multiple_window_2by2)

        self.buttonMultipleWindow3by3 = QPushButton("3-by-3-WINS")
        self.buttonMultipleWindow3by3.setEnabled(True)
        self.buttonMultipleWindow3by3.setStyleSheet("background-color: rgb(255, 250, 120);")
        self.buttonMultipleWindow3by3.clicked.connect(self.launch_multiple_window_3by3)

        self.buttonMultipleWindow4by3 = QPushButton("4-by-3-WINS")
        self.buttonMultipleWindow4by3.setEnabled(True)
        self.buttonMultipleWindow4by3.setStyleSheet("background-color: rgb(255, 250, 120);")
        self.buttonMultipleWindow4by3.clicked.connect(self.launch_multiple_window_4by3)


        self.buttonSingleWindow = QPushButton("SINGLE-WINDOW")
        self.buttonSingleWindow.setEnabled(True)
        self.buttonSingleWindow.setStyleSheet("background-color: rgb(255, 250, 120);")
        self.buttonSingleWindow.clicked.connect(self.launch_single_window)
        
        self.buttonRefresh = QPushButton("REFRESH")
        self.buttonRefresh.setEnabled(True)
        self.buttonRefresh.setStyleSheet("background-color: rgb(255, 250, 120);")
        self.buttonRefresh.clicked.connect(self.refresh)
        
        self.buttonExit = QPushButton("EXIT")
        self.buttonExit.setEnabled(True)
        self.buttonExit.setStyleSheet("background-color: rgb(255, 150, 120);")
        self.buttonExit.clicked.connect(self.exitApp)        
        
        self.vLayout.addWidget(self.label)
        self.hLayout.addWidget(self.buttonMultipleWindow2by2)
        self.hLayout.addWidget(self.buttonMultipleWindow3by3)
        self.hLayout.addWidget(self.buttonMultipleWindow4by3)
        self.hLayout.addWidget(self.buttonSingleWindow)
        self.hLayout.addWidget(self.buttonRefresh)
        self.hLayout.addWidget(self.buttonExit)

        self.layout.addLayout(self.vLayout)
        self.layout.addStretch()
        self.layout.addLayout(self.hLayout)

        self.setLayout(self.layout)
        self.showMaximized()
        self.show()

    def findScreenResolution(self):

        try:
            user32 = ctypes.windll.user32
            screenWidth = user32.GetSystemMetrics(0)
            screenHeight = user32.GetSystemMetrics(1) - HEIGHT_FACTOR

            print(f"We have read out the Screen resolution: {screenWidth}x{screenHeight}")
        except Exception as e:
            print('the screen resolution could not be determined')
            print('we proceed with these default values')
            screenWidth = SCREEN_WIDTH
            screenHeight = SCREEN_HEIGHT- HEIGHT_FACTOR
            print(f"We use the default Screen resolution: {screenWidth}x{screenHeight}")

        return [screenWidth, screenHeight]

    def refresh(self):
        self.buttonMultipleWindow2by2.setEnabled(True)
        self.buttonMultipleWindow3by3.setEnabled(True)
        self.buttonMultipleWindow4by3.setEnabled(True)

    def launch_multiple_window_2by2 (self):

        if self.buttonMultipleWindow2by2.text() == "2-by-2-WINS":
            multipleFactor = '2by2'
            self.launch_multiple_window(multipleFactor)
            return
        elif self.buttonMultipleWindow2by2.text() == "2-by-2-EXIT":
            for p in self.small_window_processes:
                print(p.name, 'name and', p.ident, ' identity of process is about to be terminated')
                p.terminate()
            self.buttonMultipleWindow2by2.setText('2-by-2-WINS')
            self.buttonMultipleWindow2by2.setEnabled(False)
            return


    def launch_multiple_window_3by3(self):
        if self.buttonMultipleWindow3by3.text() == "3-by-3-WINS":
            multipleFactor = 'pyMultiView-NDI-WinX86_64'
            self.launch_multiple_window(multipleFactor)
            return
        elif self.buttonMultipleWindow3by3.text() == "3-by-3-EXIT":
            for p in self.small_window_processes:
                print(p.name, 'name and', p.ident, ' identity of process is about to be terminated')
                p.terminate()
            self.buttonMultipleWindow3by3.setText('3-by-3-WINS')
            self.buttonMultipleWindow3by3.setEnabled(False)
            return


    def launch_multiple_window_4by3(self):
        if self.buttonMultipleWindow4by3.text() == "4-by-3-WINS":
            multipleFactor = '4by3'
            self.launch_multiple_window(multipleFactor)
            return
        elif self.buttonMultipleWindow4by3.text() == "4-by-3-EXIT":
            for p in self.small_window_processes:
                print(p.name, 'name and', p.ident, ' identity of process is about to be terminated')
                p.terminate()
            self.buttonMultipleWindow4by3.setText('4-by-3-WINS')
            self.buttonMultipleWindow4by3.setEnabled(False)
            return

    def exitApp(self):
        #print('the process list includes these processes', self.small_window_processes)
        for p in self.small_window_processes :
            print(p.name,'name and',p.ident, ' identity of process is about to be terminated')
            p.terminate()
        del self.small_window_processes
        exit(0)


    def launch_multiple_window(self, multipleFactor):

        for p in self.small_window_processes :
            print(p.name,'name and',p.ident, ' identity of process is about to be terminated')
            if p.is_alive():
                return
        self.buttonMultipleWindow2by2.setEnabled(False)
        self.buttonMultipleWindow3by3.setEnabled(False)
        self.buttonMultipleWindow4by3.setEnabled(False)


        if multipleFactor == '2by2':
            self.buttonMultipleWindow2by2.setEnabled(True)
            self.buttonMultipleWindow2by2.setText('2-by-2-EXIT')
            rowScreenCount = 2
            columnScreenCount = 2
            divisor = 1

        elif multipleFactor == 'pyMultiView-NDI-WinX86_64':
            self.buttonMultipleWindow3by3.setEnabled(True)
            self.buttonMultipleWindow3by3.setText('3-by-3-EXIT')
            rowScreenCount = 3
            columnScreenCount = 3
            divisor = 1


        elif multipleFactor == '4by3':
            self.buttonMultipleWindow4by3.setEnabled(True)
            self.buttonMultipleWindow4by3.setText('4-by-3-EXIT')
            rowScreenCount = 4
            columnScreenCount = 3
            divisor = 1

        [screenWidth, screenHeight] = self.findScreenResolution()

        win_counter = 0
        yPos = ORIG_Y_POS

        smallwindowWidth = int((screenWidth - rowScreenCount * X_FACTOR)/columnScreenCount)
        smallwindowHeight = int((screenHeight - columnScreenCount * Y_FACTOR)/rowScreenCount )

        self.winWidth = smallwindowWidth
        self.winHeight = smallwindowHeight
        self.divisor = divisor

        for i in range(rowScreenCount):
            xPos = ORIG_X_POS
            for j in range(columnScreenCount):
                win_counter = win_counter + 1
                process_name = "p" + str(win_counter)
                print("name of the process is =", process_name)
                process_name = multiprocessing.Process(target=run_generic_window, args=(
                    f"Small Window {i + j + 1}", str(smallwindowWidth), str(smallwindowHeight), str(xPos), str(yPos),str(divisor)))
                process_name.start()
                self.small_window_processes.append(process_name)
                xPos = ((j + 1) * (smallwindowWidth + X_FACTOR))
            yPos = yPos + smallwindowHeight + Y_FACTOR

    def launch_single_window(self):
        #self.buttonMultipleWindow2by2.setEnabled(False)
        #self.buttonMultipleWindow3by3.setEnabled(False)
        #self.buttonMultipleWindow4by3.setEnabled(False)
        [screenWidth, screenHeight] = self.findScreenResolution()
        print("ready to launch a new stream")
        self.count = self.count + 1
        process_name = "p" + str(self.count)
        print("name of the process is =", process_name)
        width = self.winWidth
        height = self.winHeight
        divisor = self.divisor
        process_name = multiprocessing.Process(target=run_single_window, args=(
        "SINGLE", str(width), str(height), str(ORIG_X_POS), str(ORIG_Y_POS), str(divisor)))
        process_name.start()
        self.small_window_processes.append(process_name)
        print("new stream launched successfully")
