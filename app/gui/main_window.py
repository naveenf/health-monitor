# app/gui/main_window.py

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QApplication,
                            QMessageBox, QLabel, QProgressDialog)
from PyQt6.QtGui import QScreen
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from .input_form import InputForm
from .results_view import ResultsView
from ..utils.analysis_service import AnalysisService
import logging
import time

class ModelLoadThread(QThread):
    """Thread for loading the AI model and performing AI analysis"""
    finished = pyqtSignal(dict)
    progress = pyqtSignal(int, str)
    
    def __init__(self, analysis_service, data):
        super().__init__()
        self.analysis_service = analysis_service
        self.data = data
        
    def run(self):
        try:
            # Report progress
            self.progress.emit(10, "Loading AI model...")
            
            # Get AI analysis (this handles loading the model internally)
            ai_result = self.analysis_service.get_ai_analysis(self.data)
            
            # Report completion
            self.progress.emit(100, "AI analysis complete")
            
            # Return the AI analysis result
            self.finished.emit(ai_result)
        except Exception as e:
            logging.error(f"AI analysis error: {str(e)}")
            # Return error information
            self.finished.emit({"error": str(e)})

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Health Monitoring Application")
        self.setMinimumSize(900, 700)

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
        
        # Initialize progress bar for AI analysis
        self.ai_progress = None
        
        # Center the window on screen
        self.center_window()

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
        # Show busy cursor only briefly for basic analysis
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        
        try:
            # STEP 1: Perform immediate basic analysis
            self.logger.info("Performing basic analysis...")
            
            # Get basic analysis result (this is fast)
            basic_result = self.analysis_service.get_basic_analysis(data)
            
            # Update the results view with basic analysis
            self.results_view.update_results(basic_result)
            
            # Restore cursor after basic analysis is displayed
            QApplication.restoreOverrideCursor()
            
            # STEP 2: Check if AI analysis is requested
            use_ai = data.get('preferences', {}).get('use_ai_analysis', False)
            
            if use_ai:
                # Show a small progress bar for AI analysis
                self.ai_progress = QProgressDialog("Preparing AI analysis...", "Cancel", 0, 100, self)
                self.ai_progress.setWindowTitle("AI Analysis")
                self.ai_progress.setMinimumDuration(500)  # Show after 500ms
                self.ai_progress.setValue(5)
                self.ai_progress.setWindowModality(Qt.WindowModality.NonModal)  # Allow interaction with main window
                
                # Start AI analysis in a separate thread
                self.ai_thread = ModelLoadThread(self.analysis_service, data)
                self.ai_thread.progress.connect(self.update_ai_progress)
                self.ai_thread.finished.connect(self.on_ai_analysis_complete)
                self.ai_thread.start()
                
        except Exception as e:
            self.logger.error(f"Error during analysis: {str(e)}")
            QMessageBox.critical(
                self,
                "Analysis Error",
                f"An error occurred during analysis: {str(e)}"
            )
            QApplication.restoreOverrideCursor()
    
    def update_ai_progress(self, value, message):
        """Update AI progress dialog"""
        if self.ai_progress:
            self.ai_progress.setLabelText(message)
            self.ai_progress.setValue(value)
    
    def on_ai_analysis_complete(self, ai_result):
        """
        Handle completed AI analysis and update the display.
        
        Args:
            ai_result: Dictionary with AI analysis results
        """
        # Close progress dialog
        if self.ai_progress:
            self.ai_progress.close()
            self.ai_progress = None
        
        # Check for errors
        if "error" in ai_result:
            self.logger.warning(f"AI analysis warning: {ai_result['error']}")
            # Show a small notification but don't disrupt the user experience
            QMessageBox.information(
                self,
                "AI Analysis Limited",
                "The AI analysis is limited. Basic analysis is still accurate and complete."
            )
        
        # Update the results with AI analysis
        self.results_view.add_ai_analysis(ai_result)