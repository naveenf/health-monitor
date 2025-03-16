from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QMessageBox
from PyQt6.QtCore import Qt
from .input_form import InputForm
from .results_view import ResultsView
from ..utils.analysis_service import AnalysisService
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Health Monitoring Application")
        self.setMinimumSize(800, 600)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize analysis service
        self.analysis_service = AnalysisService()

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Add input form and results view
        self.input_form = InputForm()
        self.results_view = ResultsView()

        # Connect form submission to results update
        self.input_form.submitted.connect(self.update_results)

        # Add widgets to layout
        layout.addWidget(self.input_form)
        layout.addWidget(self.results_view)

    def update_results(self, data):
        """
        Process submitted data, perform analysis, and update the results view.
        
        Args:
            data: Dictionary containing form data
        """
        # Create progress dialog with more descriptive text
        progress = QMessageBox()
        progress.setWindowTitle("Processing")
        progress.setText("Analyzing blood test results...\n\nThis may take several minutes on CPU.\nPlease be patient during first run as the AI model processes your data.")
        progress.setStandardButtons(QMessageBox.StandardButton.NoButton)
        progress.show()
        QApplication.processEvents()  # Ensure the dialog displays
        
        # Show busy cursor 
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        
        try:
            # Perform analysis on the data
            self.logger.info("Analyzing blood test results...")
            print("Starting analysis - this may take several minutes on CPU...")
            
            # Process events periodically to keep UI responsive
            analyzed_data = None
            
            # Start analysis in a separate thread to keep UI responsive
            import threading
            import time
            
            def process_data():
                nonlocal analyzed_data
                analyzed_data = self.analysis_service.analyze_results(data)
            
            analysis_thread = threading.Thread(target=process_data)
            analysis_thread.start()
            
            # Wait with timeout but keep UI responsive
            timeout = 600  # 10 minutes timeout
            start_time = time.time()
            while analysis_thread.is_alive():
                QApplication.processEvents()  # Keep UI responsive
                if time.time() - start_time > timeout:
                    raise TimeoutError("Analysis took too long to complete")
                time.sleep(0.5)  # Sleep to avoid high CPU usage
            
            # Update the results view with analyzed data
            if analyzed_data:
                self.results_view.update_results(analyzed_data)
            else:
                raise Exception("Analysis did not produce results")
                
        except TimeoutError as e:
            self.logger.error(f"Analysis timeout: {str(e)}")
            QMessageBox.critical(
                self,
                "Analysis Timeout",
                "The analysis took too long to complete. This might be due to:\n"
                "- Running on CPU instead of GPU\n"
                "- Limited memory resources\n\n"
                "Try simplifying your request or upgrading hardware."
            )
        except Exception as e:
            self.logger.error(f"Error during analysis: {str(e)}")
            QMessageBox.critical(
                self,
                "Analysis Error",
                f"An error occurred during analysis: {str(e)}"
            )
        finally:
            # Close progress dialog and restore cursor
            progress.close()
            QApplication.restoreOverrideCursor()