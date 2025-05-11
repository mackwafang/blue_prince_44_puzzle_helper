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
	QPushButton, QLineEdit, QSpacerItem, QLabel,
	QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QPalette, QColor


logging.basicConfig(level=logging.INFO)

GRID_WIDTH = 5
GRID_HEIGHT = 9
GRID_COUNT = 45
ANTICHAMBER_INDEX = 2
INTERFACE_UPDATE_FREQ = 100 # time in milliseconds
INTERFACE_AUTOSAVE_FREQ = 120000 # auto save times (2 minutes)
APP_NAME = "Blue Prince 44 Puzzle Helper"

# Subclass QMainWindow to customize your application's main window
class Puzzle44GridTab(Subtab):
	def __init__(self):
		super().__init__()

		helper.load_hints()

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
				"> Find your current location using the ingame map and located the corresponding square below.\n"
				"> Your two hints must be seperated by a comma (i.e. Honey, Apple)\n"
				"> When selecting a square, the corresponding square in the solution section and the selected square will be highlighted.\n"
				"> When your input is not valid, the border will be highlighted red when unselected.\n"
				"> After the input is validated, the square will turn yellow."
		)
		self.main_layout.addLayout(self.hints_layout) # add hints layout

		# self.main_layout.addItem(self.add_spacer(30, 30)) # add spacer

		self.create_section_title(
			self.main_layout,
			text="Solution",
			tooltip=
				"Your solution is below.\n"
				"> If your hints above has the same letter count and letters except for one, you may have the correct hints and the corresponding square willturn green.\n"
				"> Otherwise, the square will turn pink."
		)
		self.main_layout.addLayout(self.solution_layout) # add solution layout

		# disables antichamer widgets
		self.hint_input_widgets[ANTICHAMBER_INDEX].setText("Antichamber")
		self.hint_input_widgets[ANTICHAMBER_INDEX].setEnabled(False)

		# sets up timer check
		self.form_update() # update first
		self.timer = QTimer()
		self.timer.timeout.connect(self.form_update)
		self.timer.start(INTERFACE_UPDATE_FREQ) # updates every milliseconds

		self.autosave_timer = QTimer()
		self.autosave_timer.timeout.connect(self.autosave)
		self.autosave_timer.start(INTERFACE_AUTOSAVE_FREQ)

	def autosave(self):
		logging.info("Auto saving...")
		helper.save_hints()

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
				index,
				hint_input, 
				label, 
				hint_default_css="border: 1px solid black; background-color: white;",
				solution_default_css="border: 1px solid black; background-color: none;"
			)

			# guards statements
			if len(hint_input_text) == 0:
				continue

			if "," not in hint_input_text:
				hint_input.setStyleSheet(
					f"border: 1px solid {COLOR.HINT.INPUT_MISSING};"
				)
				# set specific color to antichamber
				# this is here rather than _highlight_matching_hints_and_solution
				# because the above overrides the initial call
				if index == ANTICHAMBER_INDEX:
					hint_input.setStyleSheet(
						f"border: 1px solid {COLOR.ANTICHAMBER};"
						f"background-color: {COLOR.ANTICHAMBER};"
					)

				continue

			# color hints to separate filled out fields
			if len(hint_input_text) > 0 and "," in hint_input_text:
				hint_input.setStyleSheet(
					"border: 1px solid black;"
					f"background-color: {COLOR.HINT.FILLED};"
				)

			# split the hint and update label
			hints = [i.strip() for i in hint_input_text.split(",")][:2]

			solution = helper.diff_word(*hints).upper()
			label.setText(solution)
			# set color based on solution
			style = "border: 1px solid black;"
			if len(solution) == 1:
				style += f"background-color: {COLOR.SOLUTION.EXACT}; font-weight: bold;"
				hint_input.setStyleSheet(f"background-color: {COLOR.HINT.EXACT}")
			elif len(solution) > 1:
				style += f"background-color: {COLOR.SOLUTION.CHECK};"

			label.setStyleSheet(style)
			
			self._highlight_matching_hints_and_solution(
				index,
				hint_input, 
				label, 
				hint_default_css=hint_input.styleSheet(),
				solution_default_css=label.styleSheet()
			)

	def _highlight_matching_hints_and_solution(self, index:int, hint_input:QWidget, solution:QWidget, hint_default_css="", solution_default_css=""):
		# check if focused widget is one of the inputs, highlight it and the corresponding solution label
		if self.widget.focusWidget() == hint_input:
			hint_input.setStyleSheet(
				"border: 1px solid black;"
				f"background: {COLOR.SELECT};"
			)
			solution.setStyleSheet(
				"border: 1px solid black;"
				f"background: {COLOR.SELECT};"
			)
		else:
			hint_input.setStyleSheet(hint_default_css)
			solution.setStyleSheet(solution_default_css)

			# set specific color to antichamber
			if index == ANTICHAMBER_INDEX:
				solution.setStyleSheet(
					f"border: 1px solid {COLOR.ANTICHAMBER};"
					f"background: {COLOR.ANTICHAMBER};"
				)

	def init_hint_grid(self):
		"""
		Initializes the grid for inputs
		"""
		self.hints_layout = QGridLayout()
		
		# adds input for paste hints
		self.hint_input_widgets = [self.create_input(helper.clues[i]) for i in range(GRID_COUNT)]
		self.hint_input_widget_pos = [(index // 5, (index % 5)+1) for index in range(GRID_COUNT)]
		for wi, widget in enumerate(self.hint_input_widgets):
			self.hints_layout.addWidget(widget, *self.hint_input_widget_pos[wi])

		# add rank columns in rows
		for row in range(GRID_HEIGHT):
			rank_label_settings = {"label": f"{9-row}", "css_override": "border: none; color: white;"}
			self.hints_layout.addWidget(self.create_label(**rank_label_settings), row, 0)
			self.hints_layout.addWidget(self.create_label(**rank_label_settings), row, GRID_WIDTH+1)

	def init_solution_grid(self):
		"""
		Initializes the grid for solution
		"""
		self.solution_layout = QGridLayout()

		# adds input for paste hints
		self.solution_label_widgets = [self.create_label() for i in range(GRID_COUNT)]
		self.solution_label_widget_pos = [(index // 5, (index % 5)+1) for index in range(GRID_COUNT)]
		for wi, widget in enumerate(self.solution_label_widgets):
			self.solution_layout.addWidget(widget, *self.solution_label_widget_pos[wi])

		# add rank columns in rows
		for row in range(GRID_HEIGHT):
			rank_label_settings = {"label": f"{9-row}", "css_override": "border: none; color: white;"}
			self.solution_layout.addWidget(self.create_label(**rank_label_settings), row, 0)
			self.solution_layout.addWidget(self.create_label(**rank_label_settings), row, GRID_WIDTH+1)

