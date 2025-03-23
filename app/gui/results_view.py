from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QScrollArea, QFrame, QGridLayout, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ..utils.pdf_generator import PDFGenerator

class ResultsView(QWidget):
    def __init__(self):
        super().__init__()
        # Create a scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("border: none; background-color: transparent;")

        # Create container widget for scroll area
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)  # Increase spacing between elements

        # Create a button bar for the PDF download button
        self.button_bar = QWidget()
        button_layout = QHBoxLayout(self.button_bar)
        button_layout.setContentsMargins(5, 5, 5, 10)  # Add some padding

        # Add download PDF button
        self.download_pdf_button = QPushButton("Download PDF")
        self.download_pdf_button.setStyleSheet("""
            QPushButton {
                background-color: #4a148c;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6a1b9a;
            }
            QPushButton:disabled {
                background-color: #9e9e9e;
            }
        """)
        self.download_pdf_button.clicked.connect(self.download_as_pdf)
        self.download_pdf_button.setEnabled(False)  # Disabled until we have results
        self.download_pdf_button.setFixedWidth(150)

        # Add button with right alignment
        button_layout.addStretch()
        button_layout.addWidget(self.download_pdf_button)

        # Set up main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Add button bar to main layout
        main_layout.addWidget(self.button_bar)

        # Add scroll area to main layout
        self.scroll.setWidget(self.container)
        main_layout.addWidget(self.scroll)

        # Initialize data to None
        self.current_data = None

        # Initialize PDF generator
        self.pdf_generator = PDFGenerator()

    def update_results(self, data):
        """Updates the results view to match professional medical report format"""
        # Store the data for PDF generation
        self.current_data = data

        # Enable the download button
        self.download_pdf_button.setEnabled(True)
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
            color: #ffffff;
            padding: 15px;
            background-color: #6cad7a;
            border-radius: 6px;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(header)

        # Create two-column layout for patient and specimen info
        info_layout = QHBoxLayout()
        info_layout.setSpacing(15)  # Space between columns

        # Patient Information Column
        patient_box = QWidget()
        patient_box.setStyleSheet("""
            background-color: white;
            border-radius: 6px;
            border: 1px solid #e6e6e6;
        """)
        patient_layout = QVBoxLayout(patient_box)
        patient_layout.setContentsMargins(0, 0, 0, 20)  # Remove vertical padding

        patient_header = QLabel("Patient Information")
        patient_header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1b7097;
            padding: 10px;
            text-align: center;
            background-color: #f5f5f5;
            border-bottom: 1px solid #e6e6e6;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        """)
        patient_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        patient_layout.addWidget(patient_header)

        # Get patient info
        patient_info = data.get('patient', {})
        patient_grid = QGridLayout()
        patient_grid.setContentsMargins(15, 15, 15, 15)
        patient_grid.setVerticalSpacing(10)
        patient_details = [
            ("Name:", f"{patient_info.get('first_name', '')} {patient_info.get('last_name', '')}"),
            ("Gender:", patient_info.get('gender', '')),
            ("Age:", f"{patient_info.get('age', '')} years"),
            ("Height:", f"{patient_info.get('height', '')} cm"),
            ("Weight:", f"{patient_info.get('weight', '')} kg"),
        ]

        for i, (label, value) in enumerate(patient_details):
            label_widget = QLabel(label)
            label_widget.setStyleSheet("font-weight: bold; color: #333333;")
            value_widget = QLabel(value)
            value_widget.setStyleSheet("color: #666666;")
            patient_grid.addWidget(label_widget, i, 0)
            patient_grid.addWidget(value_widget, i, 1)

        patient_layout.addLayout(patient_grid)
        info_layout.addWidget(patient_box, 1)  # Equal width
        
        # Test Information Column
        test_box = QWidget()
        test_box.setStyleSheet("""
            background-color: white;
            border-radius: 6px;
            border: 1px solid #e6e6e6;
        """)
        test_layout = QVBoxLayout(test_box)
        test_layout.setContentsMargins(0, 0, 0, 20)  # Remove vertical padding

        test_header = QLabel("Test Information")
        test_header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1b7097;
            padding: 10px;
            text-align: center;
            background-color: #f5f5f5;
            border-bottom: 1px solid #e6e6e6;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        """)
        test_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        test_layout.addWidget(test_header)

        # Get test info
        test_info = data.get('test', {})
        test_grid = QGridLayout()
        test_grid.setContentsMargins(15, 15, 15, 15)
        test_grid.setVerticalSpacing(10)
        test_details = [
            ("Lab Name:", test_info.get('lab_name', '')),
            ("Test Date:", str(test_info.get('date', ''))),
            ("Fasting State:", "Yes" if patient_info.get('fasting_state', False) else "No"),
        ]

        for i, (label, value) in enumerate(test_details):
            label_widget = QLabel(label)
            label_widget.setStyleSheet("font-weight: bold; color: #333333;")
            value_widget = QLabel(value)
            value_widget.setStyleSheet("color: #666666;")
            test_grid.addWidget(label_widget, i, 0)
            test_grid.addWidget(value_widget, i, 1)

        test_layout.addLayout(test_grid)
        info_layout.addWidget(test_box, 1)  # Equal width

        # Add info section to main layout
        info_widget = QWidget()
        info_widget.setLayout(info_layout)
        self.layout.addWidget(info_widget)

        # Create results section
        results_section = QWidget()
        results_section.setStyleSheet("""
            background-color: white;
            border-radius: 6px;
            border: 1px solid #e6e6e6;
        """)
        results_layout = QVBoxLayout(results_section)
        results_layout.setContentsMargins(0, 0, 0, 15)  # Reduce bottom padding

        # Create table headers with elegant styling
        headers_widget = QWidget()
        headers_widget.setStyleSheet("""
            background-color: #f5f5f5;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            border-bottom: 1px solid #e6e6e6;
        """)
        headers_layout = QHBoxLayout(headers_widget)
        headers_layout.setContentsMargins(15, 10, 15, 10)
        headers = ["Tests", "Result", "Reference Interval", "Units", "Status"]
        header_widths = [150, 120, 130, 120, 100]

        for i, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet("""
                font-weight: bold;
                color: #1b7097;
            """)
            label.setFixedWidth(header_widths[i])
            headers_layout.addWidget(label)

        results_layout.addWidget(headers_widget)

        # Create content widget for blood parameters
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)  # No spacing between rows for clean look

        # Add blood parameters to content
        self._add_blood_parameters(content_layout, data.get('blood_parameters', {}), header_widths)

        results_layout.addWidget(content_widget)
        self.layout.addWidget(results_section)

        # CHANGED ORDER: First add attention section for abnormal values
        self._add_attention_section(data.get('blood_parameters', {}))

        # THEN add AI analysis section if present in data
        if 'ai_analysis' in data:
            self._add_ai_analysis(data.get('ai_analysis', {}))

        # Add stretch at the end
        self.layout.addStretch()
        
    def download_as_pdf(self):
        """Handles PDF download button click"""
        if self.current_data:
            success = self.pdf_generator.generate_report(self.current_data)
            if success:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(
                    self,
                    "Success",
                    "PDF report was successfully generated."
                )

    def _add_blood_parameters(self, layout, parameters, column_widths):
        """Adds blood parameters to the layout with alternating row colors"""
        # Sort and group parameters
        grouped_params = {}
        for name, data in parameters.items():
            group = data.get('group', 'Other')
            if group not in grouped_params:
                grouped_params[group] = []
            grouped_params[group].append((name, data))

        row_index = 0
        # Display parameters by group
        for group in sorted(grouped_params.keys()):
            # Add group header
            group_header = QLabel(group)
            group_header.setStyleSheet("""
                font-weight: bold;
                color: #1b7097;
                padding: 8px 15px;
                background-color: #f8f9fa;
            """)
            layout.addWidget(group_header)
            row_index += 1

            # Add parameters
            for name, data in sorted(grouped_params[group]):
                # Create row with alternating background
                row_widget = QWidget()
                bg_color = "#ffffff" if row_index % 2 == 0 else "#f8f8f8"
                row_widget.setStyleSheet(f"background-color: {bg_color};")
                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(15, 5, 15, 5)

                # Parameter name
                name_label = QLabel(name)
                name_label.setStyleSheet("color: #333333;")
                name_label.setFixedWidth(column_widths[0])
                row_layout.addWidget(name_label)

                # Value
                value = data.get('value', 'N/A')
                value_label = QLabel(f"{value}")
                value_label.setFixedWidth(column_widths[1])
                row_layout.addWidget(value_label)

                # Reference range
                range_vals = data.get('range', [None, None])
                if range_vals and len(range_vals) == 2 and range_vals[0] is not None and range_vals[1] is not None:
                    range_str = f"{range_vals[0]}-{range_vals[1]}"
                else:
                    range_str = "Not specified"
                range_label = QLabel(range_str)
                range_label.setFixedWidth(column_widths[2])
                row_layout.addWidget(range_label)

                # Units
                unit_label = QLabel(data.get('unit', ''))
                unit_label.setFixedWidth(column_widths[3])
                row_layout.addWidget(unit_label)

                # Status
                if value != 'N/A':
                    try:
                        value_float = float(value)
                        status, color = self._get_status_and_color(value_float, data)
                    except (ValueError, TypeError) as e:
                        status, color = "Error", "#808080"
                else:
                    status, color = "No data", "#808080"

                status_label = QLabel(status)
                status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
                status_label.setFixedWidth(column_widths[4])
                row_layout.addWidget(status_label)

                layout.addWidget(row_widget)
                row_index += 1

    def _add_attention_section(self, parameters):
        """Adds a section highlighting values requiring attention with improved styling"""
        # Find parameters that are out of range
        attention_params = []

        for name, data in parameters.items():
            value = data.get('value', 'N/A')
            if value != 'N/A':
                try:
                    value_float = float(value)
                    status, color = self._get_status_and_color(value_float, data)
                    if status not in ["Normal", "No data", "Error"]:
                        attention_params.append((name, data, status, color))
                except (ValueError, TypeError):
                    continue

        if attention_params:
            # Add section container
            attention_section = QWidget()
            attention_section.setStyleSheet("""
                background-color: white;
                border-radius: 6px;
                border: 1px solid #e6e6e6;
            """)
            attention_layout = QVBoxLayout(attention_section)
            attention_layout.setContentsMargins(0, 0, 0, 15)

            # Add section header
            attention_header = QLabel("Values Requiring Attention")
            attention_header.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #1b7097;
                padding: 10px 15px;
                background-color: #f5f5f5;
                border-bottom: 1px solid #e6e6e6;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            """)
            attention_layout.addWidget(attention_header)

            # Create content for abnormal values
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(15, 15, 15, 0)
            content_layout.setSpacing(20)  # Space between entries

            for name, data, status, color in attention_params:
                # Create entry for each parameter
                param_widget = QWidget()
                param_widget.setStyleSheet("""
                    background-color: #f9f9f9;
                    border-radius: 4px;
                    padding: 5px;
                """)
                param_layout = QVBoxLayout(param_widget)
                param_layout.setContentsMargins(10, 10, 10, 10)
                param_layout.setSpacing(8)

                # Parameter header with value and status
                header_layout = QHBoxLayout()
                header = QLabel(f"{name}:")
                header.setStyleSheet("font-weight: bold; color: #1b7097;")

                value_status = QLabel(f"{data.get('value')} {data.get('unit', '')} - {status}")
                value_status.setStyleSheet(f"color: {color}; font-weight: bold;")

                header_layout.addWidget(header)
                header_layout.addWidget(value_status)
                header_layout.addStretch(1)
                param_layout.addLayout(header_layout)

                # Add separator line
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFrameShadow(QFrame.Shadow.Sunken)
                line.setStyleSheet("background-color: #e0e0e0;")
                param_layout.addWidget(line)

                # Add clinical implications
                clinical_info = data.get('clinical_info', {})
                conditions = clinical_info.get('common_conditions', {})

                implications_layout = QVBoxLayout()
                implications_title = QLabel("Possible causes:")
                implications_title.setStyleSheet("font-weight: bold; color: #666666;")
                implications_layout.addWidget(implications_title)

                if status.lower().find('low') != -1 and 'low' in conditions:
                    for condition in conditions['low']:
                        condition_label = QLabel(f"• {condition}")
                        condition_label.setStyleSheet("color: #666666; padding-left: 15px;")
                        implications_layout.addWidget(condition_label)
                elif status.lower().find('high') != -1 and 'high' in conditions:
                    for condition in conditions['high']:
                        condition_label = QLabel(f"• {condition}")
                        condition_label.setStyleSheet("color: #666666; padding-left: 15px;")
                        implications_layout.addWidget(condition_label)
                else:
                    no_info = QLabel("No additional information available")
                    no_info.setStyleSheet("color: #666666; padding-left: 15px;")
                    implications_layout.addWidget(no_info)

                param_layout.addLayout(implications_layout)

                # Add recommendations if available
                if 'test_requirements' in data:
                    reqs = data['test_requirements']
                    if isinstance(reqs, dict) and reqs.get('special_requirements'):
                        recommendations_layout = QVBoxLayout()
                        recommendations_title = QLabel("Recommendations:")
                        recommendations_title.setStyleSheet("font-weight: bold; color: #666666; margin-top: 5px;")
                        recommendations_layout.addWidget(recommendations_title)

                        for req in reqs.get('special_requirements', []):
                            req_label = QLabel(f"• {req}")
                            req_label.setStyleSheet("color: #666666; padding-left: 15px;")
                            recommendations_layout.addWidget(req_label)

                        param_layout.addLayout(recommendations_layout)

                content_layout.addWidget(param_widget)

            attention_layout.addWidget(content_widget)
            self.layout.addWidget(attention_section)

    def _add_ai_analysis(self, ai_analysis):
        """
        Updates the view with AI-powered analysis results with improved styling.

        Args:
            ai_analysis: Dictionary containing AI analysis results
        """
        if not ai_analysis or "error" in ai_analysis:
            # If there's an error or no analysis, don't display anything
            return

        # Create AI analysis section
        ai_section = QWidget()
        ai_section.setStyleSheet("""
            background-color: white;
            border-radius: 6px;
            border: 1px solid #e6e6e6;
        """)
        ai_layout = QVBoxLayout(ai_section)
        ai_layout.setContentsMargins(0, 0, 0, 15)

        # Add section header
        ai_header = QLabel("AI Analysis & Recommendations")
        ai_header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1b7097;
            padding: 10px 15px;
            background-color: #f5f5f5;
            border-bottom: 1px solid #e6e6e6;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        """)
        ai_layout.addWidget(ai_header)

        # Create content widget for sections
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 0)
        content_layout.setSpacing(15)  # Space between sections

        # Add summary section
        if ai_analysis.get("summary"):
            summary_widget = QWidget()
            summary_widget.setStyleSheet("""
                background-color: #f9f9f9;
                border-radius: 4px;
                padding: 10px;
            """)
            summary_layout = QVBoxLayout(summary_widget)
            summary_layout.setContentsMargins(10, 10, 10, 10)

            summary_header = QLabel("Summary")
            summary_header.setStyleSheet("font-weight: bold; color: #1b7097;")
            summary_layout.addWidget(summary_header)

            summary_text = QLabel(ai_analysis["summary"])
            summary_text.setWordWrap(True)
            summary_text.setStyleSheet("color: #333333; padding: 5px 0;")
            summary_layout.addWidget(summary_text)

            content_layout.addWidget(summary_widget)

        # Function to add a section with title and items
        def add_section(title, items, icon_color="#1b7097"):
            if not items:
                return

            section_widget = QWidget()
            section_widget.setStyleSheet("""
                background-color: #f9f9f9;
                border-radius: 4px;
                padding: 10px;
            """)
            section_layout = QVBoxLayout(section_widget)
            section_layout.setContentsMargins(10, 10, 10, 10)

            section_header = QLabel(title)
            section_header.setStyleSheet(f"font-weight: bold; color: {icon_color};")
            section_layout.addWidget(section_header)

            for item in items:
                item_layout = QHBoxLayout()
                bullet = QLabel("•")
                bullet.setStyleSheet(f"color: {icon_color}; font-weight: bold;")

                text = QLabel(item)
                text.setWordWrap(True)
                text.setStyleSheet("color: #333333;")

                item_layout.addWidget(bullet)
                item_layout.addWidget(text, 1)  # Give text stretch factor

                section_layout.addLayout(item_layout)

            content_layout.addWidget(section_widget)

        # Add sections using the add_section function
        add_section("Abnormal Values Analysis", ai_analysis.get("abnormal_values", []), "#FFA500")  # Orange
        add_section("Health Implications", ai_analysis.get("implications", []), "#1b7097")  # Blue
        add_section("Recommendations", ai_analysis.get("recommendations", []), "#6cad7a")  # Green
        add_section("Suggested Follow-up Tests", ai_analysis.get("followup_tests", []))

        # Add disclaimer
        disclaimer = QLabel("AI-generated analysis is for informational purposes only and should not replace professional medical advice.")
        disclaimer.setWordWrap(True)
        disclaimer.setStyleSheet("color: #FF5722; font-style: italic; padding: 10px; font-size: 11px;")
        content_layout.addWidget(disclaimer)

        ai_layout.addWidget(content_widget)
        self.layout.addWidget(ai_section)

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
    
    def add_ai_analysis(self, ai_analysis):
        """
        Add AI analysis to an existing results display.
        
        Args:
            ai_analysis: Dictionary containing AI analysis data
        """
        if not self.current_data:
            return  # No data to update
        
        # Add AI analysis to current data
        self.current_data["ai_analysis"] = ai_analysis
        
        # Update the display with the combined data
        self.update_results(self.current_data)