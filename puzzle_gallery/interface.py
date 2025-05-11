import sys

import logging

from puzzle_gallery import helper

from icecream import ic

from common.subtab import Subtab
from typing import Union, Optional
from PyQt6.QtCore import QSize, QUrl, Qt, QTimer
from PyQt6.QtWidgets import (
	QApplication,
	QWidget, QMainWindow, QLayout,
	QPushButton, QLineEdit, QScrollArea, QLabel,
	QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QPalette, QColor

GRID_HEIGHT = 8
GRID_WIDTH = 8
GRID_COUNT = 64

class PuzzleGalleryTab(Subtab):
	def __init__(self):
		super().__init__()
		
		self.main_layout = QVBoxLayout()
		self.widget.setLayout(self.main_layout)

		self.init_hint_grid()
		self.init_solution_grid()
		
		####################################
		# POST LAYOUT INIT
		####################################
		self.create_section_title(
			self.main_layout, 
			text="Hints", 
			tooltip=
				"Place your hints in a square.\n"
		)
		self.main_layout.addLayout(self.hints_layout) # add hints layout

		# adds submit button
		self.hint_submit_button = self.create_button("Submit")
		self.hint_submit_button.setStyleSheet(
			"background-color: white;"
		)
		self.hint_submit_button.released.connect(self._submit_hints)
		self.main_layout.addWidget(self.hint_submit_button)

		# adds clear button
		self.hint_clear_button = self.create_button("Clear")
		self.hint_clear_button.setStyleSheet(
			"background-color: white;"
		)
		self.hint_clear_button.released.connect(self._clear_hints)
		self.main_layout.addWidget(self.hint_clear_button)


		self.create_section_title(
			self.main_layout,
			text="Solution",
			tooltip=
				"Your solution is below.\n"
		)
		self.main_layout.addLayout(self.solution_layout) # add solution layout
	
	def init_hint_grid(self):
		self.hints_layout = QGridLayout()
		
		# adds input for paste hints
		self.hint_input_widgets = [self.create_input() for i in range(GRID_COUNT)]
		self.hint_input_widget_pos = [(index // GRID_WIDTH, index % GRID_WIDTH) for index in range(GRID_COUNT)]
		for wi, widget in enumerate(self.hint_input_widgets):
			widget.setMaxLength(1)
			widget.textChanged.connect(self._cursor_automove)
			widget.setFixedSize(QSize(32,  32))
			widget.setPlaceholderText("")
			# overriding css
			widget.setStyleSheet(
				"background-color: white;"
				"font-weight: bold;"
				"text-transform: uppercase;"
			)

			# adding input
			self.hints_layout.addWidget(widget, *self.hint_input_widget_pos[wi])
		
	def _submit_hints(self):
		logging.info("Submitted gallery hints")

		hints = [i.text() for i in self.hint_input_widgets]
		hints = [''.join(hints[col::GRID_WIDTH]) for col in range(GRID_WIDTH)]
			
		solution_length = sum(1 for h in hints if len(h) > 0)
		solutions = helper.create_possible_words([col for col in hints if len(col) > 0], solution_length)
		
		logging.info(f"Found {len(solutions)} solutions")

		self.solution_label_widget.setText("\n".join(f"<b>{k.upper()}</b>: {', '.join(v)}<br/><br/>" for k, v in solutions.items()))

	def _clear_hints(self):
		for i in self.hint_input_widgets:
			i.setText("")
	
	def _cursor_automove(self):
		if len(self.widget.focusWidget().text()) == 1:
			self.widget.focusNextChild()

	def init_solution_grid(self):
		self.solution_layout = QVBoxLayout()

		self.solution_label_widget = self.create_label("", css_override="color: white;")
		self.solution_label_widget.setFixedSize(500, 10000)
		self.solution_label_widget.setWordWrap(True)
		self.solution_label_widget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

		# self.solution_label_widget.setWordWrap(True)
		# self.solution_layout.addWidget(self.solution_label_widget)
		
		self.solution_scroll_area = QScrollArea()
		self.solution_scroll_area.setWidget(self.solution_label_widget)
		self.solution_layout.addWidget(self.solution_scroll_area)
