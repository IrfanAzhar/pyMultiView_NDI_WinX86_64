import sys
from PyQt6.QtWidgets import QApplication
from GenericWindowClass import GenericWindow

def run_generic_window(title, width, height, xPos, yPos, divisor):
   app = QApplication(sys.argv)
   single_window = GenericWindow(title, width, height, xPos, yPos,divisor)
   sys.exit(app.exec())
