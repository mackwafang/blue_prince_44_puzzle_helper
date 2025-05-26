import sys

import logging

from puzzle_44_grid import helper
from puzzle_44_grid.color import COLOR

from common.subtab import Subtab
from typing import Union, Optional
from PyQt6.QtCore import QSize, QUrl, Qt, QTimer
from PyQt6.QtWidgets import (
	QApplication,
	QWidget, QMainWindow, QLayout,
	QLabel, QComboBox,
	QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QPalette, QColor, QIcon


logging.basicConfig(level=logging.INFO)

GRID_WIDTH = 5
GRID_HEIGHT = 9
GRID_COUNT = 45
ANTICHAMBER_INDEX = 2
INTERFACE_UPDATE_FREQ = 100 # time in milliseconds
INTERFACE_AUTOSAVE_FREQ = 120000 # auto save times (2 minutes)

# Subclass QMainWindow to customize your application's main window
class PuzzleChess(Subtab):
	def __init__(self):
		super().__init__()

		self.chess_pieces = {
			" ": "-",
			"k": "King",
			"q": "Queen",
			"r": "Rook",
			"b": "Bishop",
			"n": "Knight",
			"p": "Pawn"
		}
		self.chess_images = {k: QIcon(f"puzzle_chess/img/{v}.png") for k, v in self.chess_pieces.items()}

		self.main_layout = QVBoxLayout()
		self.widget.setLayout(self.main_layout)

		self.init_chess_grid()

		self.main_layout.addLayout(self.chess_layout)

	def create_chess_combo_box(self):
		combobox = QComboBox()
		combobox.setStyleSheet(
				"background-color: #ddd;"
		)
		combobox.setFixedSize(64, 64)

		for chess_piece in self.chess_pieces:
			combobox.addItem(self.chess_images[chess_piece], self.chess_pieces[chess_piece])

		return combobox

	def init_chess_grid(self):
		"""
			Initializes the manson's grid to allow to put chess pieces in 
		"""
		self.chess_layout = QGridLayout()
		
		# adds input for paste hints
		self.hint_input_widgets = [self.create_chess_combo_box() for i in range(GRID_COUNT)]
		self.hint_input_widget_pos = [(index // 5, (index % 5)+1) for index in range(GRID_COUNT)]
		for wi, widget in enumerate(self.hint_input_widgets):
			self.chess_layout.addWidget(widget, *self.hint_input_widget_pos[wi])

		# add rank columns in rows
		for row in range(GRID_HEIGHT):
			rank_label_settings = {"label": f"{9-row}", "css_override": "border: none; color: white;"}
			self.chess_layout.addWidget(self.create_label(**rank_label_settings), row, 0)
			self.chess_layout.addWidget(self.create_label(**rank_label_settings), row, GRID_WIDTH+1)
