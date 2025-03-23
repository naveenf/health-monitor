# app/utils/pdf_generator.py
from PyQt6.QtWidgets import QFileDialog
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
import datetime

class PDFGenerator:
    """
    Utility class for generating PDF reports from blood test results
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        # Create a custom style for headers
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=14,
            spaceAfter=10,
            textColor=colors.purple,
        ))
        # Create a custom style for section headers
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=12,
            spaceAfter=6,
            textColor=colors.purple,
        ))

    def generate_report(self, data, filename=None):
        """
        Generate a PDF report from the provided data

        Args:
            data: Dictionary containing patient info, test info, and blood parameters
            filename: Optional filename to save the PDF, if None a file dialog will be shown

        Returns:
            bool: True if report was generated successfully, False otherwise
        """
        
        # Add debugging for AI analysis
        print("\n===== DEBUG: PDF Generation Data =====")
        print(f"Data keys: {data.keys()}")
        if 'ai_analysis' in data:
            print(f"AI Analysis present, type: {type(data['ai_analysis'])}")
            if isinstance(data['ai_analysis'], dict):
                print(f"AI Analysis keys: {data['ai_analysis'].keys()}")
                for key, value in data['ai_analysis'].items():
                    print(f"  {key}: {type(value)} with {len(value) if hasattr(value, '__len__') else 'N/A'} items")
        else:
            print("AI Analysis NOT present in data")
        print("====================================\n")

        if not filename:
            filename, _ = QFileDialog.getSaveFileName(
                None,
                "Save PDF Report",
                f"Health_Report_{datetime.datetime.now().strftime('%Y%m%d')}.pdf",
                "PDF Files (*.pdf)"
            )

        if not filename:
            return False  # User cancelled the dialog

        if not filename.endswith(".pdf"):
            filename += ".pdf"

        try:
            # Create document
            doc = SimpleDocTemplate(
                filename,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            # Build content
            elements = []

            # Add title
            title = Paragraph("Blood Test Results Report", self.styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 0.25*inch))

            # Add patient information
            elements.append(Paragraph("Patient Information", self.styles['CustomHeading']))
            patient_info = data.get('patient', {})
            patient_data = [
                ["Name:", f"{patient_info.get('first_name', '')} {patient_info.get('last_name', '')}"],
                ["Gender:", patient_info.get('gender', '')],
                ["Age:", f"{patient_info.get('age', '')} years"],
                ["Height:", f"{patient_info.get('height', '')} cm"],
                ["Weight:", f"{patient_info.get('weight', '')} kg"],
            ]

            patient_table = Table(patient_data, colWidths=[1.5*inch, 4*inch])
            patient_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lavender),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(patient_table)
            elements.append(Spacer(1, 0.1*inch))

            # Add test information
            elements.append(Paragraph("Test Information", self.styles['CustomHeading']))
            test_info = data.get('test', {})
            test_data = [
                ["Lab Name:", test_info.get('lab_name', '')],
                ["Test Date:", str(test_info.get('date', ''))],
                ["Fasting State:", "Yes" if patient_info.get('fasting_state', False) else "No"],
            ]

            test_table = Table(test_data, colWidths=[1.5*inch, 4*inch])
            test_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lavender),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(test_table)
            elements.append(Spacer(1, 0.25*inch))

            # Add Values Requiring Attention section
            # Collect abnormal parameters
            abnormal_params = []
            for name, param_info in data.get('blood_parameters', {}).items():
                value = param_info.get('value', 'N/A')
                if value != 'N/A':
                    try:
                        value_float = float(value)
                        range_vals = param_info.get('range', [None, None])
                        if range_vals and len(range_vals) == 2:
                            min_val, max_val = range_vals

                            if min_val is not None and max_val is not None:
                                min_val = float(min_val)
                                max_val = float(max_val)

                                if value_float < min_val or value_float > max_val:
                                    abnormal_params.append((name, param_info))
                    except (ValueError, TypeError):
                        pass

            # Add abnormal values section if there are any
            if abnormal_params:
                elements.append(Paragraph("Values Requiring Attention", self.styles['CustomHeading']))

                for name, param_info in abnormal_params:
                    # Parameter name and value
                    value = param_info.get('value', 'N/A')
                    unit = param_info.get('unit', '')

                    # Get range
                    range_vals = param_info.get('range', [None, None])
                    if range_vals and len(range_vals) == 2:
                        min_val, max_val = range_vals[0], range_vals[1]

                    # Determine status
                    if value != 'N/A':
                        try:
                            value_float = float(value)
                            if min_val is not None and max_val is not None:
                                min_val = float(min_val)
                                max_val = float(max_val)

                                status = ""
                                if value_float < min_val:
                                    deviation = ((min_val - value_float) / min_val) * 100
                                    if deviation > 20:
                                        status = "Very Low"
                                    else:
                                        status = "Low"
                                elif value_float > max_val:
                                    deviation = ((value_float - max_val) / max_val) * 100
                                    if deviation > 20:
                                        status = "Very High"
                                    else:
                                        status = "High"
                        except (ValueError, TypeError):
                            status = "Error"

                    # Create header for this parameter
                    param_header = Paragraph(f"{name}: {value} {unit} - {status}", self.styles['SectionHeading'])
                    elements.append(param_header)

                    # Add clinical implications
                    clinical_info = param_info.get('clinical_info', {})
                    conditions = clinical_info.get('common_conditions', {})

                    if status.lower().find('low') != -1 and 'low' in conditions:
                        elements.append(Paragraph("Possible causes:", self.styles['Heading4']))
                        for condition in conditions['low']:
                            elements.append(Paragraph(f"• {condition}", self.styles['Normal']))
                    elif status.lower().find('high') != -1 and 'high' in conditions:
                        elements.append(Paragraph("Possible causes:", self.styles['Heading4']))
                        for condition in conditions['high']:
                            elements.append(Paragraph(f"• {condition}", self.styles['Normal']))

                    # Add recommendations if available
                    if 'test_requirements' in param_info:
                        reqs = param_info['test_requirements']
                        if isinstance(reqs, list) and reqs:
                            elements.append(Paragraph("Recommendations:", self.styles['Heading4']))
                            for req in reqs:
                                elements.append(Paragraph(f"• {req}", self.styles['Normal']))

                    elements.append(Spacer(1, 0.2*inch))

                elements.append(Spacer(1, 0.1*inch))

            # Add blood parameters by group
            elements.append(Paragraph("Blood Test Parameters", self.styles['CustomHeading']))

            # Group parameters
            grouped_params = {}
            for name, param_data in data.get('blood_parameters', {}).items():
                group = param_data.get('group', 'Other')
                if group not in grouped_params:
                    grouped_params[group] = []
                grouped_params[group].append((name, param_data))

            # Create a table for each group
            for group in sorted(grouped_params.keys()):
                elements.append(Paragraph(group, self.styles['SectionHeading']))

                # Create table header
                param_data = [["Parameter", "Value", "Reference Range", "Units", "Status"]]

                # Add parameters for this group
                for name, param_info in sorted(grouped_params[group]):
                    value = param_info.get('value', 'N/A')
                    unit = param_info.get('unit', '')

                    # Get range
                    range_vals = param_info.get('range', [None, None])
                    if range_vals and len(range_vals) == 2:
                        range_str = f"{range_vals[0]}-{range_vals[1]}"
                    else:
                        range_str = "Not specified"

                    # Get status
                    status = ""
                    if value != 'N/A':
                        try:
                            value_float = float(value)
                            min_val, max_val = range_vals

                            if min_val is not None and max_val is not None:
                                min_val = float(min_val)
                                max_val = float(max_val)

                                if value_float < min_val:
                                    deviation = ((min_val - value_float) / min_val) * 100
                                    if deviation > 20:
                                        status = "Very Low"
                                    else:
                                        status = "Low"
                                elif value_float > max_val:
                                    deviation = ((value_float - max_val) / max_val) * 100
                                    if deviation > 20:
                                        status = "Very High"
                                    else:
                                        status = "High"
                                else:
                                    status = "Normal"
                            else:
                                status = "No range"
                        except (ValueError, TypeError):
                            status = "Error"
                    else:
                        status = "No data"

                    param_data.append([name, str(value), range_str, unit, status])

                # Create and style the table
                param_table = Table(param_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 1.25*inch, 0.75*inch])

                # Define table styles with colors based on status
                table_style = [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lavender),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]

                # Add row-specific styling based on status
                for i in range(1, len(param_data)):
                    status = param_data[i][4]
                    if status == "Normal":
                        table_style.append(('TEXTCOLOR', (4, i), (4, i), colors.green))
                    elif status in ["Low", "High", "Borderline"]:
                        table_style.append(('TEXTCOLOR', (4, i), (4, i), colors.orange))
                    elif status in ["Very Low", "Very High", "Critical"]:
                        table_style.append(('TEXTCOLOR', (4, i), (4, i), colors.red))

                param_table.setStyle(TableStyle(table_style))
                elements.append(param_table)
                elements.append(Spacer(1, 0.2*inch))

            # Add AI analysis section AFTER the blood parameters section
            # This is moved OUTSIDE the loop so it isn't dependent on the last group iteration
            if 'ai_analysis' in data:
                ai_analysis = data.get('ai_analysis', {})
                
                # Add debug prints to see what we're working with
                print(f"AI Analysis data type: {type(ai_analysis)}")
                print(f"AI Analysis keys: {ai_analysis.keys() if isinstance(ai_analysis, dict) else 'Not a dictionary'}")
                
                # More robust check for content availability
                has_summary = ai_analysis.get("summary", "") if isinstance(ai_analysis, dict) else False
                has_abnormal = ai_analysis.get("abnormal_values", []) if isinstance(ai_analysis, dict) else []
                has_implications = ai_analysis.get("implications", []) if isinstance(ai_analysis, dict) else []
                has_recommendations = ai_analysis.get("recommendations", []) if isinstance(ai_analysis, dict) else []
                has_followup = ai_analysis.get("followup_tests", []) if isinstance(ai_analysis, dict) else []
                
                if has_summary or has_abnormal or has_implications or has_recommendations or has_followup:
                    elements.append(Spacer(1, 0.1*inch))
                    elements.append(Paragraph("AI Analysis & Recommendations", self.styles['CustomHeading']))

                    # Add summary
                    if has_summary:
                        elements.append(Paragraph("Summary", self.styles['SectionHeading']))
                        elements.append(Paragraph(str(has_summary), self.styles['Normal']))
                        elements.append(Spacer(1, 0.1*inch))

                    # Add abnormal values analysis
                    if has_abnormal:
                        elements.append(Paragraph("Abnormal Values Analysis", self.styles['SectionHeading']))
                        for item in has_abnormal:
                            elements.append(Paragraph(f"• {item}", self.styles['Normal']))
                        elements.append(Spacer(1, 0.1*inch))

                    # Add health implications
                    if has_implications:
                        elements.append(Paragraph("Health Implications", self.styles['SectionHeading']))
                        for item in has_implications:
                            elements.append(Paragraph(f"• {item}", self.styles['Normal']))
                        elements.append(Spacer(1, 0.1*inch))

                    # Add recommendations
                    if has_recommendations:
                        elements.append(Paragraph("Recommendations", self.styles['SectionHeading']))
                        for item in has_recommendations:
                            elements.append(Paragraph(f"• {item}", self.styles['Normal']))
                        elements.append(Spacer(1, 0.1*inch))

                    # Add follow-up tests
                    if has_followup:
                        elements.append(Paragraph("Suggested Follow-up Tests", self.styles['SectionHeading']))
                        for item in has_followup:
                            elements.append(Paragraph(f"• {item}", self.styles['Normal']))
                        elements.append(Spacer(1, 0.1*inch))

                    # Add disclaimer
                    disclaimer = "AI-generated analysis is for informational purposes only and should not replace professional medical advice."
                    elements.append(Paragraph(disclaimer, self.styles['Italic']))
                else:
                    print("AI analysis is present in data but contains no content")
            else:
                print("No AI analysis found in data")

            # Add medical disclaimer at the end
            elements.append(Spacer(1, 0.5*inch))
            disclaimer_text = "DISCLAIMER: This report is for informational purposes only and should not be used for diagnosis or treatment decisions. Please consult with a healthcare professional for interpretation of these results."
            elements.append(Paragraph(disclaimer_text, self.styles['Italic']))

            # Add timestamp
            elements.append(Spacer(1, 0.2*inch))
            timestamp = f"Report generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            elements.append(Paragraph(timestamp, self.styles['Normal']))

            # Build the document
            doc.build(elements)
            return True

        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return False
        