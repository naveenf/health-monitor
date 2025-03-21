from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFormLayout,
                             QComboBox, QCheckBox, QGroupBox,
                             QDateEdit, QSpinBox, QDoubleSpinBox,
                             QMessageBox, QScrollArea, QTabWidget,
                             QHBoxLayout, QFrame)
from PyQt6.QtCore import pyqtSignal, Qt, QDate
from PyQt6.QtGui import QFont, QColor
from app.model.parameters.parameter_definitions import BLOOD_PARAMETERS


class PatientInfoSection(QGroupBox):
    """Group box containing patient's basic information"""

    def __init__(self, parent=None):
        super().__init__("Patient Information", parent)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        layout.setSpacing(12)  # Increase spacing
        layout.setContentsMargins(15, 15, 15, 15)  # Add padding

        # Apply a stylesheet to the group box
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 15px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                min-height: 25px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #4CAF50;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        # Name fields
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.first_name.setPlaceholderText("Required")
        self.last_name.setPlaceholderText("Required")

        # Gender dropdown
        self.gender = QComboBox()
        self.gender.addItems(["Select Gender", "Male", "Female"])

        # Age spinbox
        self.age = QSpinBox()
        self.age.setRange(0, 120)

        # Height and Weight
        self.height = QDoubleSpinBox()
        self.height.setRange(0, 300)
        self.height.setSuffix(" cm")

        self.weight = QDoubleSpinBox()
        self.weight.setRange(0, 500)
        self.weight.setSuffix(" kg")

        # Fasting checkbox
        self.fasting_state = QCheckBox("Fasting State (8+ hours)")
        self.fasting_state.setStyleSheet("""
            QCheckBox {
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)

        # Add fields to layout
        layout.addRow("First Name*:", self.first_name)
        layout.addRow("Last Name*:", self.last_name)
        layout.addRow("Gender*:", self.gender)
        layout.addRow("Age*:", self.age)
        layout.addRow("Height:", self.height)
        layout.addRow("Weight:", self.weight)
        layout.addRow(self.fasting_state)

        self.setLayout(layout)


class TestInfoSection(QGroupBox):
    """Group box containing test-related information"""

    def __init__(self, parent=None):
        super().__init__("Test Information", parent)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Apply the same styling as PatientInfoSection
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 15px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QDateEdit, QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                min-height: 25px;
            }
            QDateEdit:focus, QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        # Test date
        self.test_date = QDateEdit()
        self.test_date.setDate(QDate.currentDate())
        self.test_date.setCalendarPopup(True)
        self.test_date.setStyleSheet("""
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #ccc;
            }
        """)

        # Lab name
        self.lab_name = QLineEdit()

        # Add fields to layout
        layout.addRow("Test Date*:", self.test_date)
        layout.addRow("Lab Name:", self.lab_name)

        self.setLayout(layout)


class BloodParametersSection(QGroupBox):
    """Group box containing blood test parameters organized by categories"""

    def __init__(self, parent=None):
        super().__init__("Blood Test Parameters", parent)
        self.parameter_inputs = {}  # Store all input fields
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        tabs = QTabWidget()

        # Style the tabs
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e0e0e0;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                min-height: 25px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        # Apply styling to the groupbox itself
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 15px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        # Continue with your existing code for creating tabs
        for group_name, group_data in BLOOD_PARAMETERS.items():
            tab = QWidget()
            form_layout = QFormLayout()
            form_layout.setSpacing(12)

            # Sort parameters by order if available
            parameters = sorted(
                group_data['parameters'].items(),
                key=lambda x: x[1].get('display', {}).get('order', float('inf'))
            )

            # Create alternating row containers for zebra striping
            row_index = 0
            for param_name, param_info in parameters:
                # Create row container with alternating background
                row_container = QWidget()
                row_bg_color = "#f8f8f8" if row_index % 2 == 0 else "#ffffff"
                row_container.setStyleSheet(f"background-color: {row_bg_color};")
                row_layout = QHBoxLayout(row_container)
                row_layout.setContentsMargins(5, 5, 5, 5)

                # Create input field with validation
                input_field = QLineEdit()
                input_field.setFixedWidth(120)
                input_field.setFixedHeight(24)
                unit_label = QLabel(param_info['unit']['standard'])
                unit_label.setStyleSheet("color: #333333; font-size: 11px;")

                # Get ranges
                ranges = param_info.get('ranges', {})

                # Build placeholder text showing relevant ranges
                placeholder_parts = []

                # Add standard range if available
                if 'standard' in ranges:
                    std_range = ranges['standard']
                    min_val = std_range.get('min', 'N/A')
                    max_val = std_range.get('max', 'N/A')
                    placeholder_parts.append(f"{min_val}-{max_val}")

                placeholder = "".join(placeholder_parts) if placeholder_parts else ""
                input_field.setPlaceholderText(placeholder)

                # Add tooltip with additional information
                tooltip = self._create_tooltip(param_name, param_info)
                input_field.setToolTip(tooltip)

                # Parameter name and input field
                param_label = QLabel(f"{param_name}:")
                param_label.setStyleSheet("color: #333333; font-size: 13px;")
                param_label.setFixedWidth(180)

                # Range label
                range_text = f"Range: {placeholder}" if placeholder else ""
                range_label = QLabel(range_text)
                range_label.setStyleSheet("color: #888888; font-size: 11px;")
                range_label.setFixedWidth(130)

                # Add to row layout
                row_layout.addWidget(param_label)
                row_layout.addWidget(input_field)
                row_layout.addWidget(range_label)
                row_layout.addWidget(unit_label)
                row_layout.addStretch(1)  # Add stretch to push everything to the left

                # Add row to form layout
                form_layout.addRow(row_container)

                # Store input field reference with full parameter name
                self.parameter_inputs[param_name] = input_field

                # Increment row index for alternating backgrounds
                row_index += 1

            tab.setLayout(form_layout)
            tabs.addTab(tab, group_name)

        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    def _create_tooltip(self, param_name, param_info):
        """Creates enhanced tooltip with detailed information"""
        # Create sections for the tooltip
        tooltip_sections = []

        # Get basic metadata and clinical info
        metadata = param_info.get('metadata', {})
        clinical_info = param_info.get('clinical_info', {})

        # Add description
        description = clinical_info.get('description')
        if description:
            tooltip_sections.append(description)

        # Add function if available
        function = clinical_info.get('function')
        if function:
            tooltip_sections.append(f"\nFunction: {function}")

        # Add common conditions
        conditions = clinical_info.get('common_conditions', {})
        if conditions:
            tooltip_sections.append("\nCommon conditions:")
            if 'high' in conditions:
                high_conditions = ", ".join(conditions['high'])
                tooltip_sections.append(f"High: {high_conditions}")
            if 'low' in conditions:
                low_conditions = ", ".join(conditions['low'])
                tooltip_sections.append(f"Low: {low_conditions}")

        # Add test requirements
        test_reqs = param_info.get('test_requirements', {})
        if isinstance(test_reqs, dict):  # If test_requirements is a dictionary
            if test_reqs:
                tooltip_sections.append("\nTest requirements:")
                if test_reqs.get('fasting_required'):
                    tooltip_sections.append(f"• Fasting required: {test_reqs.get('fasting_duration', '')} hours")
                if test_reqs.get('special_requirements'):
                    for req in test_reqs['special_requirements']:
                        tooltip_sections.append(f"• {req}")

                # Add interfering factors if present
                interfering = test_reqs.get('interfering_factors', [])
                if interfering:
                    tooltip_sections.append("\nInterfering factors:")
                    for factor in interfering:
                        tooltip_sections.append(f"• {factor}")
        elif isinstance(test_reqs, list):  # If test_requirements is a list
            if test_reqs:
                tooltip_sections.append("\nTest requirements:")
                for req in test_reqs:
                    tooltip_sections.append(f"• {req}")

        # Join all sections with newlines
        tooltip_text = "\n".join(tooltip_sections)

        # If no content was added, provide a default message
        if not tooltip_text:
            tooltip_text = "No additional information available"

        return tooltip_text

    def get_values(self):
        """Returns dictionary of all parameter values"""
        values = {}
        for param_name, input_field in self.parameter_inputs.items():
            text = input_field.text().strip()
            if text:
                try:
                    values[param_name] = float(text)
                except ValueError:
                    pass
        return values


class InputForm(QWidget):
    # Signal to emit when form is submitted
    submitted = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Apply modern stylesheet to scroll area
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
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

        # Create container widget
        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(20, 20, 20, 20)  # Add more padding
        self.layout.setSpacing(15)  # Increase spacing between elements

        # Add patient info section
        self.patient_info = PatientInfoSection()
        self.layout.addWidget(self.patient_info)

        # Add test info section
        self.test_info = TestInfoSection()
        self.layout.addWidget(self.test_info)

        # Add blood parameters section
        self.blood_params = BloodParametersSection()
        self.layout.addWidget(self.blood_params)

        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setStyleSheet("color: red; margin-top: 10px;")
        self.layout.addWidget(required_note)

        # Add submit button with improved styling
        self.submit_button = QPushButton("Submit Results")
        self.submit_button.setMinimumHeight(40)  # Make button taller
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)
        self.submit_button.clicked.connect(self.on_submit)
        self.layout.addWidget(self.submit_button)

        # Add some space at the bottom
        self.layout.addSpacing(30)

        # Set the container as the scroll area's widget
        scroll.setWidget(container)

        # Main layout for the form
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

        # Add AI analysis option
        self.ai_analysis_checkbox = QCheckBox("Use AI analysis for recommendations")
        self.ai_analysis_checkbox.setChecked(True)  # Enable by default
        self.ai_analysis_checkbox.setStyleSheet("""
            QCheckBox {
                color: #666666;
                margin-top: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #6cad7a;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                background-color: #6cad7a;
            }
        """)
        self.layout.addWidget(self.ai_analysis_checkbox)


    def _validate_required_fields(self) -> bool:
        """Validates that all required fields are filled"""
        missing_fields = []

        if not self.patient_info.first_name.text():
            missing_fields.append("First Name")
        if not self.patient_info.last_name.text():
            missing_fields.append("Last Name")
        if self.patient_info.gender.currentText() == "Select Gender":
            missing_fields.append("Gender")
        if self.patient_info.age.value() == 0:
            missing_fields.append("Age")

        if missing_fields:
            QMessageBox.warning(
                self,
                "Required Fields Missing",
                f"Please fill in the following required fields:\n• " +
                "\n• ".join(missing_fields)
            )
            return False
        return True

    def on_submit(self):
        if not self._validate_required_fields():
            return

        try:
            # Get all blood parameter values
            blood_parameters = self.blood_params.get_values()

            # Create data dictionary
            data = {
                'patient': {
                    'first_name': self.patient_info.first_name.text(),
                    'last_name': self.patient_info.last_name.text(),
                    'gender': self.patient_info.gender.currentText(),
                    'age': self.patient_info.age.value(),
                    'height': self.patient_info.height.value(),
                    'weight': self.patient_info.weight.value(),
                    'fasting_state': self.patient_info.fasting_state.isChecked()
                },
                'test': {
                    'date': self.test_info.test_date.date().toPyDate(),
                    'lab_name': self.test_info.lab_name.text()
                },
                'blood_parameters': {},
                'preferences': {
                    'use_ai_analysis': self.ai_analysis_checkbox.isChecked()
                }
            }

            # Add each parameter with its metadata and properly formatted ranges
            for param_name, value in blood_parameters.items():
                # Find the group this parameter belongs to
                for group_name, group_data in BLOOD_PARAMETERS.items():
                    group_params = group_data['parameters']
                    if param_name in group_params:
                        param_info = group_params[param_name]

                        # Get appropriate range based on gender
                        gender = self.patient_info.gender.currentText().lower()
                        ranges = param_info.get('ranges', {})

                        # First try to get from standard ranges
                        if 'standard' in ranges:
                            range_min = ranges['standard'].get('min')
                            range_max = ranges['standard'].get('max')
                        # Then try gender-specific ranges
                        elif 'gender_specific' in ranges and gender in ranges['gender_specific']:
                            gender_range = ranges['gender_specific'][gender]
                            range_min = gender_range.get('min')
                            range_max = gender_range.get('max')
                        # Finally try base ranges if they exist
                        elif 'base' in ranges:
                            if isinstance(ranges['base'], dict):
                                if gender in ranges['base']:
                                    range_min = ranges['base'][gender].get('min')
                                    range_max = ranges['base'][gender].get('max')
                                else:
                                    # If no gender-specific range, use the first available range
                                    first_range = next(iter(ranges['base'].values()))
                                    range_min = first_range.get('min')
                                    range_max = first_range.get('max')
                            else:
                                range_min = None
                                range_max = None
                        else:
                            range_min = None
                            range_max = None

                        data['blood_parameters'][param_name] = {
                            'value': value,
                            'unit': param_info['unit']['standard'],
                            'group': group_name,
                            'range': [range_min, range_max],
                            'metadata': param_info.get('metadata', {}),
                            'clinical_info': param_info.get('clinical_info', {})
                        }
                        break

            # Emit the data
            self.submitted.emit(data)

        except ValueError as e:
            QMessageBox.warning(
                self,
                "Invalid Input",
                f"Please enter valid numbers for blood parameters: {str(e)}"
            )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"An error occurred while processing the form: {str(e)}"
            )

    def clear_form(self):
        """Clears all form fields"""
        # Clear patient info
        self.patient_info.first_name.clear()
        self.patient_info.last_name.clear()
        self.patient_info.gender.setCurrentIndex(0)
        self.patient_info.age.setValue(0)
        self.patient_info.height.setValue(0)
        self.patient_info.weight.setValue(0)
        self.patient_info.fasting_state.setChecked(False)

        # Clear test info
        self.test_info.test_date.setDate(QDate.currentDate())
        self.test_info.lab_name.clear()

        # Clear blood parameters
        for input_field in self.blood_params.parameter_inputs.values():
            input_field.clear()
