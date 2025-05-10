import sys
sys.path.append("common")
sys.path.append("puzzle_44_grid")

import logging

from puzzle_44_grid.interface import Puzzle44GridWindow

from common.window import MainWindow
from typing import Union, Optional
from PyQt6.QtCore import QSize, QUrl, Qt, QTimer
from PyQt6.QtWidgets import (
	QApplication,
	QWidget, QMainWindow, QLayout,
	QLabel, QTabWidget,
	QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QPalette, QColor


APP_NAME = "Blue Prince Helper"
logging.basicConfig(level=logging.INFO)

class MainWindow(MainWindow):
	def __init__(self):
		super().__init__()

	def init_ui(self):
		super().init_ui()

		self.tab = QTabWidget()
		
		# initialize tabs
		self.puzzle_44_grid_window = Puzzle44GridWindow()
		self.tab.addTab(self.puzzle_44_grid_window.widget, "44 Grids")

		self.main_layout.addWidget(self.tab)
		
		self.widget = QWidget()
		self.widget.setLayout(self.main_layout)

		self.setCentralWidget(self.widget)

	def init_style(self):
		palette = QPalette()
		palette.setColor(QPalette.ColorRole.Window, QColor(32, 32, 32, 255))
		palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255, 255))
		self.setPalette(palette)

if __name__ == "__main__":

	app = QApplication(sys.argv)
	app.setApplicationName(APP_NAME)

	window = MainWindow()
	window.show()

	app.exec()
