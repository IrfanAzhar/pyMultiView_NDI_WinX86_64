import sys
from PyQt6.QtWidgets import QApplication
from SingleWindowClass import SingleWindow

def run_single_window(title, width, height, xPos, yPos, divisor):
   app = QApplication(sys.argv)
   single_window = SingleWindow(title, width, height, xPos, yPos, divisor)
   sys.exit(app.exec())
