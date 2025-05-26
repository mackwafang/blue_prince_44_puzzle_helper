import sys
import logging

from puzzle_44_grid.interface import Puzzle44GridTab
from puzzle_gallery.interface import PuzzleGalleryTab
from puzzle_chess.interface import PuzzleChess

from typing import Union, Optional
from PyQt6.QtCore import QSize, QUrl, Qt, QTimer
from PyQt6.QtWidgets import (
	QApplication,
	QWidget, QMainWindow,
	QLabel, QTabWidget,
	QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QPalette, QColor


APP_NAME = "Blue Prince Helper"
logging.basicConfig(level=logging.INFO)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.init_ui()
		self.init_style()

	def init_ui(self):
		self.WINDOW_WIDTH = 500
		self.WINDOW_HEIGHT = 500

		self.tab = QTabWidget()
		self.main_layout = QVBoxLayout()
		
		# initialize tabs
		self.puzzle_44_grid_tab = Puzzle44GridTab()
		self.tab.addTab(self.puzzle_44_grid_tab.widget, "44 Grids")
		
		self.puzzle_gallery_tab = PuzzleGalleryTab()
		self.tab.addTab(self.puzzle_gallery_tab.widget, "Gallery")

		self.puzzle_chess = PuzzleChess()
		self.tab.addTab(self.puzzle_chess.widget, "Chess")
		

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

	# save hints when window close
	window.puzzle_44_grid_tab.save_hints()
