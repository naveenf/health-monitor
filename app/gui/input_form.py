from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFormLayout,
                             QComboBox, QCheckBox, QGroupBox,
                             QDateEdit, QSpinBox, QDoubleSpinBox,
                             QMessageBox, QScrollArea, QTabWidget,
                             QHBoxLayout)
from PyQt6.QtCore import pyqtSignal, Qt, QDate
from app.model.parameters.parameter_definitions import BLOOD_PARAMETERS


class PatientInfoSection(QGroupBox):
    """Group box containing patient's basic information"""

    def __init__(self, parent=None):
        super().__init__("Patient Information", parent)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

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

        # Test date
        self.test_date = QDateEdit()
        self.test_date.setDate(QDate.currentDate())
        self.test_date.setCalendarPopup(True)

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
        tabs = QTabWidget()

        # Create tabs for each parameter group
        for group_name, group_data in BLOOD_PARAMETERS.items():
            tab = QWidget()
            form_layout = QFormLayout()

            # Sort parameters by order if available
            parameters = sorted(
                group_data['parameters'].items(),
                key=lambda x: x[1].get('display', {}).get('order', float('inf'))
            )

            # Add parameters for this group
            for param_name, param_info in parameters:
                # Create input field with validation
                input_field = QLineEdit()
                unit_label = QLabel(param_info['unit']['standard'])

                # Get ranges
                ranges = param_info.get('ranges', {})

                # Build placeholder text showing relevant ranges
                placeholder_parts = []

                # Add standard range if available
                if 'standard' in ranges:
                    std_range = ranges['standard']
                    placeholder_parts.append(f"Standard: {std_range.get('min', 'N/A')}-{std_range.get('max', 'N/A')}")

                # Add gender-specific ranges if available
                if 'gender_specific' in ranges:
                    gender_ranges = ranges['gender_specific']
                    if 'male' in gender_ranges:
                        male_range = gender_ranges['male']
                        placeholder_parts.append(f"M: {male_range.get('min', 'N/A')}-{male_range.get('max', 'N/A')}")
                    if 'female' in gender_ranges:
                        female_range = gender_ranges['female']
                        placeholder_parts.append(f"F: {female_range.get('min', 'N/A')}-{female_range.get('max', 'N/A')}")

                placeholder = " | ".join(placeholder_parts) if placeholder_parts else "No range specified"
                input_field.setPlaceholderText(placeholder)

                # Add tooltip with additional information
                tooltip = self._create_tooltip(param_name, param_info)
                input_field.setToolTip(tooltip)

                # Create horizontal layout for input and unit
                input_layout = QHBoxLayout()
                input_layout.addWidget(input_field)
                input_layout.addWidget(unit_label)

                # Set fixed widths for better alignment
                input_field.setFixedWidth(150)
                unit_label.setFixedWidth(100)

                # Add to form layout with some spacing
                label = QLabel(f"{param_name}:")
                label.setFixedWidth(120)
                form_layout.addRow(label, input_layout)

                # Store input field reference with full parameter name
                self.parameter_inputs[param_name] = input_field

            # Add some spacing to the form layout
            form_layout.setSpacing(10)
            form_layout.setContentsMargins(10, 10, 10, 10)

            tab.setLayout(form_layout)
            tabs.addTab(tab, group_name)

        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    def _create_tooltip(self, param_name, param_info):
        """Creates enhanced tooltip with more detailed information"""
        metadata = param_info.get('metadata', {})
        clinical_info = param_info.get('clinical_info', {})

        tooltip = []
        tooltip.append(metadata.get('description', 'No description available'))
        tooltip.append(f"\nFunction: {clinical_info.get('function', 'Not specified')}")

        # Add common conditions
        conditions = clinical_info.get('common_conditions', {})
        if conditions:
            tooltip.append("\nCommon conditions:")
            if 'high' in conditions:
                tooltip.append("High: " + ", ".join(conditions['high']))
            if 'low' in conditions:
                tooltip.append("Low: " + ", ".join(conditions['low']))

        # Add test requirements
        requirements = param_info.get('test_requirements', {})
        if requirements:
            tooltip.append("\nTest requirements:")
            if requirements.get('fasting_required'):
                tooltip.append(f"• Fasting required: {requirements['fasting_duration']} hours")
            if requirements.get('special_requirements'):
                tooltip.append("• " + "\n• ".join(requirements['special_requirements']))

        # Add interfering factors
        if 'interfering_factors' in requirements:
            tooltip.append("\nInterfering factors:")
            tooltip.append("• " + "\n• ".join(requirements['interfering_factors']))

        return "\n".join(tooltip)

    def get_values(self):
        """Returns dictionary of all parameter values"""
        values = {}
        for param_name, input_field in self.parameter_inputs.items():
            #print(f"Getting value for {param_name}")  # Debug print
            text = input_field.text().strip()
            if text:
                try:
                    values[param_name] = float(text)
                    #print(f"  Value: {values[param_name]}")  # Debug print
                except ValueError:
                    #print(f"  Invalid value for {param_name}: {text}")  # Debug print
                    pass
        return values

    def _get_appropriate_range(self, param_info, patient_data):
        """Gets the appropriate range based on patient characteristics"""
        ranges = param_info.get('ranges', {})
        gender = patient_data.get('gender', '').lower()
        age = patient_data.get('age', 0)

        # Check condition-specific ranges first (if implemented)
        if 'condition_specific' in ranges:
            # Logic for condition-specific ranges would go here
            pass

        # Check age-specific ranges
        if 'age_specific' in ranges:
            age_ranges = ranges['age_specific']
            if age <= 1:
                return age_ranges.get('newborn', {})
            elif age <= 12:
                return age_ranges.get('child', {})
            elif age >= 65:
                return age_ranges.get('elderly', {})
            else:
                return age_ranges.get('adult', {})

        # Fall back to gender-specific ranges
        if 'gender_specific' in ranges:
            return ranges['gender_specific'].get(gender, {})

        # Finally, fall back to standard range
        return ranges.get('standard', {})


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

        # Create container widget
        container = QWidget()
        self.layout = QVBoxLayout(container)

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
        required_note.setStyleSheet("color: red;")
        self.layout.addWidget(required_note)

        # Add submit button
        self.submit_button = QPushButton("Submit Results")
        self.submit_button.clicked.connect(self.on_submit)
        self.layout.addWidget(self.submit_button)

        # Add stretch at the end
        self.layout.addStretch()

        # Set the container as the scroll area's widget
        scroll.setWidget(container)

        # Main layout for the form
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

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
                'blood_parameters': {}
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
        self.blood_params.rbc_input.clear()
        self.blood_params.wbc_input.clear()
