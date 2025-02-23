from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from .input_form import InputForm
from .results_view import ResultsView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Health Monitoring Application")
        self.setMinimumSize(800, 600)

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
        # Update the results view with the submitted data
        self.results_view.update_results(data)