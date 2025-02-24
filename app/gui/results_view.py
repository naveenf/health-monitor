from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QScrollArea, QFrame, QGridLayout)
from PyQt6.QtCore import Qt

class ResultsView(QWidget):
    def __init__(self):
        super().__init__()
        # Create a scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Create container widget for scroll area
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)

        # Set up main layout
        main_layout = QVBoxLayout(self)

        # Add scroll area to main layout
        self.scroll.setWidget(self.container)
        main_layout.addWidget(self.scroll)

    def update_results(self, data):
        """Updates the results view to match professional medical report format"""
        # Clear previous results
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Create header section with title
        header = QLabel("Blood Test Results")
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #4a148c;
            padding: 10px;
            background-color: #f5f5f5;
            border-bottom: 2px solid #4a148c;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(header)

        # Create two-column layout for patient and specimen info
        info_layout = QHBoxLayout()

        # Patient Information Column
        patient_box = QWidget()
        patient_layout = QVBoxLayout(patient_box)

        patient_header = QLabel("Patient Information")
        patient_header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #4a148c;
            padding: 10px;
            text-align: center;
            background-color: #f5f5f5;
            border-bottom: 1px solid #4a148c;
        """)
        patient_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        patient_layout.addWidget(patient_header)

        # Get patient info
        patient_info = data.get('patient', {})
        patient_grid = QGridLayout()
        patient_details = [
            ("Name:", f"{patient_info.get('first_name', '')} {patient_info.get('last_name', '')}"),
            ("Gender:", patient_info.get('gender', '')),
            ("Age:", f"{patient_info.get('age', '')} years"),
            ("Height:", f"{patient_info.get('height', '')} cm"),
            ("Weight:", f"{patient_info.get('weight', '')} kg"),
        ]

        for i, (label, value) in enumerate(patient_details):
            label_widget = QLabel(label)
            label_widget.setStyleSheet("font-weight: bold; padding: 5px;")
            value_widget = QLabel(value)
            value_widget.setStyleSheet("padding: 5px;")
            patient_grid.addWidget(label_widget, i, 0)
            patient_grid.addWidget(value_widget, i, 1)

        patient_layout.addLayout(patient_grid)
        info_layout.addWidget(patient_box)

        # Test Information Column
        test_box = QWidget()
        test_layout = QVBoxLayout(test_box)

        test_header = QLabel("Test Information")
        test_header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #4a148c;
            padding: 10px;
            text-align: center;
            background-color: #f5f5f5;
            border-bottom: 1px solid #4a148c;
        """)
        test_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        test_layout.addWidget(test_header)

        # Get test info
        test_info = data.get('test', {})
        test_grid = QGridLayout()
        test_details = [
            ("Lab Name:", test_info.get('lab_name', '')),
            ("Test Date:", str(test_info.get('date', ''))),
            ("Fasting State:", "Yes" if patient_info.get('fasting_state', False) else "No"),
        ]

        for i, (label, value) in enumerate(test_details):
            label_widget = QLabel(label)
            label_widget.setStyleSheet("font-weight: bold; padding: 5px;")
            value_widget = QLabel(value)
            value_widget.setStyleSheet("padding: 5px;")
            test_grid.addWidget(label_widget, i, 0)
            test_grid.addWidget(value_widget, i, 1)

        test_layout.addLayout(test_grid)
        info_layout.addWidget(test_box)

        # Add info section to main layout
        info_widget = QWidget()
        info_widget.setLayout(info_layout)
        info_widget.setStyleSheet("""
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            margin: 10px;
            padding: 10px;
        """)
        self.layout.addWidget(info_widget)

        # Create table headers
        headers_widget = QWidget()
        headers_layout = QHBoxLayout(headers_widget)
        headers = ["Tests", "Result", "Reference Interval", "Units", "Status"]

        for header in headers:
            label = QLabel(header)
            label.setStyleSheet("""
                font-weight: bold;
                padding: 5px;
                border-bottom: 1px solid #e0e0e0;
            """)
            if header == "Tests":
                label.setFixedWidth(150)
            elif header == "Status":
                label.setFixedWidth(100)
            else:
                label.setFixedWidth(120)
            headers_layout.addWidget(label)

        self.layout.addWidget(headers_widget)

        # Update blood parameters
        self.update_blood_parameters(data.get('blood_parameters', {}))

        # Add stretch at the end
        self.layout.addStretch()

    def update_blood_parameters(self, parameters):
        """Updates the blood parameters display"""
        # Sort and group parameters
        grouped_params = {}
        for name, data in parameters.items():
            group = data.get('group', 'Other')
            if group not in grouped_params:
                grouped_params[group] = []
            grouped_params[group].append((name, data))

        # Display parameters by group
        for group in sorted(grouped_params.keys()):
            # Add group header
            group_widget = QWidget()
            group_layout = QVBoxLayout(group_widget)
            group_layout.setSpacing(2)  # Reduce spacing between items

            group_header = QLabel(group)
            group_header.setStyleSheet("""
                font-weight: bold;
                color: #4a148c;
                padding: 5px;
                background-color: #f8f9fa;
            """)
            group_layout.addWidget(group_header)

            # Add parameters
            for name, data in sorted(grouped_params[group]):
                # Create main parameter row
                param_container = QWidget()
                param_layout = QVBoxLayout(param_container)
                param_layout.setSpacing(0)  # Minimal spacing between elements
                param_layout.setContentsMargins(0, 0, 0, 5)  # Add bottom margin only

                # Parameter values row
                values_widget = QWidget()
                row_layout = QHBoxLayout(values_widget)
                row_layout.setContentsMargins(5, 2, 5, 2)

                # Parameter name
                name_label = QLabel(name)
                name_label.setFixedWidth(150)
                row_layout.addWidget(name_label)

                # Value
                value = data.get('value', 'N/A')
                value_label = QLabel(f"{value}")
                value_label.setFixedWidth(120)
                row_layout.addWidget(value_label)

                # Reference range
                range_vals = data.get('range', [None, None])
                if range_vals and len(range_vals) == 2:
                    range_str = f"{range_vals[0]}-{range_vals[1]}"
                else:
                    range_str = "Not specified"
                range_label = QLabel(range_str)
                range_label.setFixedWidth(120)
                row_layout.addWidget(range_label)

                # Units
                unit_label = QLabel(data.get('unit', ''))
                unit_label.setFixedWidth(120)
                row_layout.addWidget(unit_label)

                # Status
                if value != 'N/A':
                    try:
                        value_float = float(value)
                        status, color = self._get_status_and_color(value_float, data)
                    except (ValueError, TypeError) as e:
                        print(f"Error processing value for {name}: {e}")
                        status, color = "Error", "#808080"
                else:
                    status, color = "No data", "#808080"

                status_label = QLabel(status)
                status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
                status_label.setFixedWidth(100)
                row_layout.addWidget(status_label)

                # Add the values row to the parameter container
                param_layout.addWidget(values_widget)

                # Add metadata if value is out of range
                if status not in ["Normal", "No data", "Error"]:
                    metadata_widget = self._create_parameter_detail_widget(name, data)
                    if metadata_widget:
                        param_layout.addWidget(metadata_widget)

                # Add the complete parameter container to the group
                group_layout.addWidget(param_container)

            self.layout.addWidget(group_widget)


    def _create_parameter_detail_widget(self, name, data):
        """Creates a detail widget for out-of-range parameters"""
        metadata = data.get('metadata', {})
        clinical_info = data.get('clinical_info', {})
        if not metadata and not clinical_info:
            return None

        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(20, 5, 5, 5)  # Add left indent and some vertical spacing

        # Create sections container
        sections_widget = QWidget()
        sections_layout = QVBoxLayout(sections_widget)
        sections_layout.setSpacing(8)  # Space between sections

        # Add description if available
        if metadata.get('description'):
            desc_label = QLabel(metadata['description'])
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #666666; font-style: italic; font-size: 11px;")
            sections_layout.addWidget(desc_label)

        # Add common conditions based on status
        value = float(data.get('value', 0))
        range_vals = data.get('range', [None, None])
        
        if range_vals and len(range_vals) == 2:
            min_val, max_val = float(range_vals[0]), float(range_vals[1])
            conditions = []
            condition_title = ""
            
            if value < min_val and 'low' in clinical_info.get('common_conditions', {}):
                conditions = clinical_info['common_conditions']['low']
                condition_title = "Common conditions for low values:"
            elif value > max_val and 'high' in clinical_info.get('common_conditions', {}):
                conditions = clinical_info['common_conditions']['high']
                condition_title = "Common conditions for high values:"
                
            if conditions:
                conditions_text = f"{condition_title}\n• " + "\n• ".join(conditions)
                cond_label = QLabel(conditions_text)
                cond_label.setWordWrap(True)
                cond_label.setStyleSheet("color: #FFA500; font-size: 11px;")
                sections_layout.addWidget(cond_label)

        # Add test requirements if available
        test_reqs = metadata.get('test_requirements', [])
        if test_reqs:
            reqs_label = QLabel("Test Requirements:\n• " + "\n• ".join(test_reqs))
            reqs_label.setWordWrap(True)
            reqs_label.setStyleSheet("color: #666666; font-size: 11px;")
            sections_layout.addWidget(reqs_label)

        # Add the sections to the main layout
        detail_layout.addWidget(sections_widget)
        
        return detail_widget

    def _get_status_and_color(self, value, param_info):
        """Enhanced status determination using range values"""
        try:
            # Get range values from the parameter info
            range_vals = param_info.get('range', [None, None])
            if not range_vals or len(range_vals) != 2:
                return "No range", "#808080"

            min_val, max_val = range_vals

            if min_val is None or max_val is None:
                return "No range", "#808080"

            # Convert to float to ensure proper comparison
            min_val = float(min_val)
            max_val = float(max_val)

            # Calculate percentage deviation
            if value < min_val:
                deviation = ((min_val - value) / min_val) * 100
                if deviation > 20:
                    return "Very Low", "#FF0000"  # Red
                return "Low", "#FFA500"  # Orange
            elif value > max_val:
                deviation = ((value - max_val) / max_val) * 100
                if deviation > 20:
                    return "Very High", "#FF0000"  # Red
                return "High", "#FFA500"  # Orange
            else:
                return "Normal", "#008000"  # Green

        except Exception as e:
            print(f"Error calculating status: {e}")
            return "Error", "#808080"

    def _get_status_display(self, classification):
        """Maps classifications to display values"""
        status_map = {
            'very_low': ("Very Low", "#FF0000"),
            'low': ("Low", "#FFA500"),
            'normal': ("Normal", "#008000"),
            'high': ("High", "#FFA500"),
            'very_high': ("Very High", "#FF0000"),
            'optimal': ("Optimal", "#008000"),
            'borderline': ("Borderline", "#FFA500"),
            'critical': ("Critical", "#FF0000")
        }
        return status_map.get(classification, ("Unknown", "#808080"))
