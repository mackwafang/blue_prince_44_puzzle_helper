import sys

from typing import Union, Optional
from PyQt6.QtCore import QSize, QUrl, Qt, QTimer
from PyQt6.QtWidgets import (
	QApplication,
	QWidget, QMainWindow, QLayout,
	QPushButton, QLineEdit, QSpacerItem, QLabel,
	QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QPalette, QColor

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.init_ui()
		self.init_style()

	def init_ui(self):
		self.WINDOW_WIDTH = 500
		self.WINDOW_HEIGHT = 500
		self.main_layout = QVBoxLayout()

	def init_style(self):
		palette = QPalette()
		palette.setColor(QPalette.ColorRole.Window, QColor(32, 32, 32, 255))
		palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255, 255))
		self.setPalette(palette)

	

	def create_section_title(self, parent_layout: QLayout, text="", tooltip=""):
		layout_title_widget = self.create_label(text)
		layout_title_widget.setToolTip(tooltip)
		layout_title_widget.setStyleSheet(
		"""
		QLabel {
			border: none;
			font-size: 32px;
			font-weight: bold;
			color: white;
		}
		QToolTip  {
			background-color: white;
			font-size: 12px;
			font-weight: normal;
		}
		"""
		)
		layout_title_widget.setFixedSize(QSize(200,  40))

		layout = QHBoxLayout()
		layout.addWidget(layout_title_widget)
		parent_layout.addLayout(layout)

	def create_button(self, text=""):
		button = QPushButton(text)
		
		return button

	def create_input(self, text=""):
		"""
		Create input fields
		"""
		text_field = QLineEdit(text)
		text_field.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		text_field.setFixedSize(QSize(100,  50))
		text_field.setPlaceholderText("Hint1 Hint2")
		return text_field

	def create_label(self, label="", css_override=""):
		"""
		Create labels fields
		"""
		label = QLabel(label)
		label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		label.setFixedSize(QSize(60,  30))
		label.setStyleSheet(
			"border: 1px solid black;" if not css_override else css_override
		)
		return label

	def add_spacer(self, width: int, height: int):
		spacer = QSpacerItem(width, height)	
		return spacer
