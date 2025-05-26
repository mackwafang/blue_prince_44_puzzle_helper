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
from PyQt6.QtGui import QPalette, QColor, QIcon, QPixmap


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

		self.chess_data = {}
		for piece in self.chess_pieces:
			self.chess_data[piece] = {
				"img": QIcon(f"puzzle_chess/img/{self.chess_pieces[piece]}.png"),
				"status_img": QPixmap(f"puzzle_chess/img/{self.chess_pieces[piece]}_white.png"),
				"count": 0,
				"widget": self.create_label("0", css_override="color: white; font-weight: bold; font-size: 32px"),
			}

		self.main_layout = QVBoxLayout()
		self.widget.setLayout(self.main_layout)

		self.init_chess_grid()
		self.init_status_bar()

		self.init_clear_button()

		self.autosave_timer = QTimer()
		self.autosave_timer.timeout.connect(self.form_update)
		self.autosave_timer.start(INTERFACE_UPDATE_FREQ)
		

	def form_update(self):
		# reset all counts
		for piece in self.chess_pieces:
			self.chess_data[piece]['count'] = 0

		# count all of the chess pieces
		for widget in self.chess_input_widgets:
			key = list(self.chess_data.keys())[widget.currentIndex()]
			self.chess_data[key]['count'] += 1
			
		# update all of the widgets
		for piece in self.chess_pieces:
			self.chess_data[piece]['widget'].setText(str(self.chess_data[piece]['count']))

	def create_chess_combo_box(self):
		combobox = QComboBox()
		combobox.setStyleSheet(
				"background-color: #ddd;"
		)
		combobox.setFixedSize(96, 64)

		for chess_piece in self.chess_pieces:
			combobox.addItem(self.chess_data[chess_piece]['img'], self.chess_pieces[chess_piece])

		return combobox

	def init_clear_button(self):
		self.clear_button = self.create_button("Clear")
		self.clear_button.setStyleSheet("background-color: white")
		self.clear_button.released.connect(self._clear_board)
		self.main_layout.addWidget(self.clear_button)

	def _clear_board(self):
		for widget in self.chess_input_widgets:
			widget.setCurrentIndex(0)

	def init_chess_grid(self):
		"""
			Initializes the manson's grid to allow to put chess pieces in 
		"""
		self.chess_layout = QGridLayout()
		
		# adds input for paste hints
		self.chess_input_widgets = [self.create_chess_combo_box() for i in range(GRID_COUNT)]
		self.chess_input_widget_pos = [(index // 5, (index % 5)+1) for index in range(GRID_COUNT)]
		for wi, widget in enumerate(self.chess_input_widgets):
			self.chess_layout.addWidget(widget, *self.chess_input_widget_pos[wi])

		# add rank columns in rows
		for row in range(GRID_HEIGHT):
			rank_label_settings = {"label": f"{9-row}", "css_override": "border: none; color: white;"}
			self.chess_layout.addWidget(self.create_label(**rank_label_settings), row, 0)
			self.chess_layout.addWidget(self.create_label(**rank_label_settings), row, GRID_WIDTH+1)

		self.main_layout.addLayout(self.chess_layout)

	def init_status_bar(self):
		self.chess_status_layout = QGridLayout()
		
		for index, piece in enumerate(self.chess_pieces):
			if index == 0:
				continue

			label = self.create_label(css_override="border:none;")
			label.setPixmap(self.chess_data[piece]['status_img'])

			self.chess_status_layout.addWidget(label, 0, (index*2))
			self.chess_status_layout.addWidget(self.chess_data[piece]['widget'], 1, (index*2))

		self.main_layout.addLayout(self.chess_status_layout)
