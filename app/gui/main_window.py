# app/gui/main_window.py

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QApplication,
                            QMessageBox, QLabel)
from PyQt6.QtGui import QScreen
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from .input_form import InputForm
from .results_view import ResultsView
from ..utils.analysis_service import AnalysisService
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Health Monitoring Application")
        self.setMinimumSize(900, 700)  # Increase default size

        # Set application-wide stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #6c757d;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Add application title
        title_label = QLabel("Health Monitor")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            background-color: #4CAF50;
            padding: 10px;
            border-radius: 5px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize analysis service
        self.analysis_service = AnalysisService()

        # Add input form and results view
        self.input_form = InputForm()
        self.results_view = ResultsView()

        # Connect form submission to results update
        self.input_form.submitted.connect(self.update_results)

        # Add widgets to layout
        layout.addWidget(self.input_form)
        layout.addWidget(self.results_view)

    def setup_fonts(self):
        """Set up custom fonts for the application"""
        # For headers (equivalent to Playfair Display in the design)
        header_font = QFont("Serif", 14)
        header_font.setBold(True)

        # For regular text (equivalent to Lato in the design)
        text_font = QFont("Sans", 10)

        # Apply fonts to application
        QApplication.setFont(text_font)

    def setup_stylesheet(self):
        """Apply stylesheet to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f8f8;
            }
            QGroupBox {
                border: 1px solid #e6e6e6;
                border-radius: 6px;
                margin-top: 1.5ex;
                background-color: white;
            }
            QGroupBox::title {
                color: #1b7097;
                font-size: 16px;
                font-weight: bold;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 10px;
            }
            QPushButton {
                background-color: #6cad7a;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5c9d6a;
            }
            QPushButton:pressed {
                background-color: #4c8d5a;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
                border: 1px solid #e6e6e6;
                border-radius: 4px;
                padding: 6px;
                min-height: 24px;
            }
            QTabWidget::pane {
                border: 1px solid #e6e6e6;
                border-radius: 6px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding: 8px 16px;
                color: #666666;
            }
            QTabBar::tab:selected {
                background-color: #1b7097;
                color: white;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QLabel {
                color: #333333;
            }
        """)

    def center_window(self):
        """Center the main window on the screen"""
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def update_results(self, data):
        """
        Process submitted data, perform analysis, and update the results view.

        Args:
            data: Dictionary containing form data
        """
        # Show busy cursor while processing
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        try:
            # Perform analysis on the data
            self.logger.info("Analyzing blood test results...")
            analyzed_data = self.analysis_service.analyze_results(data)

            # Update the results view with analyzed data
            self.results_view.update_results(analyzed_data)

        except Exception as e:
            self.logger.error(f"Error during analysis: {str(e)}")
            QMessageBox.critical(
                self,
                "Analysis Error",
                f"An error occurred during analysis: {str(e)}"
            )
        finally:
            # Restore cursor
            QApplication.restoreOverrideCursor()
