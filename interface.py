import sys

from icecream import ic
from typing import Union, Optional
from PyQt6.QtCore import QSize, QUrl, Qt, QTimer
from PyQt6.QtWidgets import (
	QApplication,
	QWidget,QMainWindow,
	QPushButton, QLineEdit, QSpacerItem, QLabel,
	QVBoxLayout, QGridLayout, QSizePolicy
)
import logging
import helper

logging.basicConfig(level=logging.INFO)

GRID_WIDTH = 5
GRID_HEIGHT = 9
GRID_COUNT = 45
INTERFACE_UPDATE_FREQ = 100 # time in milliseconds
APP_NAME = "Blue Prince 44 Puzzle Helper"

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		self.WINDOW_WIDTH = 500
		self.WINDOW_HEIGHT = 500
		self.main_layout = QVBoxLayout()

		self.init_hint_grid()
		self.init_solution_grid()

		####################################
		# POST LAYOUT INIT
		####################################
		self.main_layout.addLayout(self.hints_layout) # add hints layout
		self.main_layout.addItem(self.add_spacer(30, 30)) # add spacer
		self.main_layout.addLayout(self.solution_layout) # add solution layout


		self.widget = QWidget()
		self.widget.setLayout(self.main_layout)

		self.setCentralWidget(self.widget)

		# sets up timer check
		self.form_update() # update first
		self.timer = QTimer()
		self.timer.timeout.connect(self.form_update)
		self.timer.start(INTERFACE_UPDATE_FREQ) # updates every milliseconds

	def form_update(self):
		"""
		Handler for when the timer checks
		"""
		# updates label with hints after helper removed same letters
		for index in range(GRID_COUNT):
			hint_input = self.hint_input_widgets[index]
			label = self.solution_label_widgets[index]
			hint_input_text = hint_input.text()

			# set default stylesheet for widgets
			self._highlight_matching_hints_and_solution(
				hint_input, 
				label, 
				hint_default_css="border: 1px solid black; background: white;",
				solution_default_css="border: 1px solid black; background: none;"
			)

			# guards statements
			if len(hint_input_text) == 0:
				continue

			if "," not in hint_input_text:
				hint_input.setStyleSheet(
					"border: 1px solid red;"
				)
				continue

			# color hints to separate filled out fields
			if len(hint_input_text) > 0 and "," in hint_input_text:
				hint_input.setStyleSheet(
					"border: 1px solid black;"
					"background: yellow;"
				)

			# split the hint and update label
			hints = [i.strip() for i in hint_input_text.split(",")][:2]

			solution = helper.diff_word(*hints).upper()
			label.setText(solution)
			# set color based on solution
			style = "border: 1px solid black;"
			if len(solution) == 1:
				style += "background-color: #0f0; font-weight: bold;"
			elif len(solution) > 1:
				style += "background-color: pink;"

			label.setStyleSheet(style)

			
			self._highlight_matching_hints_and_solution(
				hint_input, 
				label, 
				hint_default_css=hint_input.styleSheet(),
				solution_default_css=label.styleSheet()
			)

	def _highlight_matching_hints_and_solution(self, hint_input:QWidget, solution:QWidget, hint_default_css="", solution_default_css=""):
		# check if focused widget is one of the inputs, highlight it and the corresponding solution label
		if self.focusWidget() == hint_input:
			hint_input.setStyleSheet(
				"border: 1px solid #aaf;"
				"background: #aaf;"
			)
			solution.setStyleSheet(
				"border: 1px solid #aaf;"
				"background: #aaf;"
			)
		else:
			hint_input.setStyleSheet(hint_default_css)
			solution.setStyleSheet(solution_default_css)

	def init_hint_grid(self):
		"""
		Initializes the grid for inputs
		"""
		self.hints_layout = QGridLayout()

		# adds input for paste hints
		self.hint_input_widgets = [self.create_input(helper.clues[i]) for i in range(GRID_COUNT)]
		self.hint_input_widget_pos = [(index // 5, index % 5) for index in range(GRID_COUNT)]
		for wi, widget in enumerate(self.hint_input_widgets):
			self.hints_layout.addWidget(widget, *self.hint_input_widget_pos[wi])

	def init_solution_grid(self):
		"""
		Initializes the grid for solution
		"""
		self.solution_layout = QGridLayout()

		# adds input for paste hints
		self.solution_label_widgets = [self.create_label() for i in range(GRID_COUNT)]
		self.solution_label_widget_pos = [(index // 5, index % 5) for index in range(GRID_COUNT)]
		for wi, widget in enumerate(self.solution_label_widgets):
			self.solution_layout.addWidget(widget, *self.solution_label_widget_pos[wi])

	def create_input(self, text=""):
		"""
		Create input fields
		"""
		text_field = QLineEdit(text)
		text_field.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		text_field.setFixedSize(QSize(100,  50))
		text_field.setPlaceholderText("Hint1 Hint2")
		return text_field

	def create_label(self):
		"""
		Create labels fields
		"""
		label = QLabel()
		label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		label.setFixedSize(QSize(60,  30))
		label.setStyleSheet(
			"border: 1px solid black;"
			""
		)
		return label

	def add_spacer(self, width: int, height: int):
		spacer = QSpacerItem(width, height)
		return spacer

if __name__ == "__main__":
	helper.load_hints()

	app = QApplication(sys.argv)
	app.setApplicationName(APP_NAME)

	window = MainWindow()
	window.show()

	app.exec()

	helper.clues = [i.text() for i in window.hint_input_widgets]
	helper.save_hints()
