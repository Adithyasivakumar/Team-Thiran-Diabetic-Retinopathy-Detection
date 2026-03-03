"""
PDF Report Generator for Medical Records
Creates professional medical-grade PDF reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from datetime import datetime
import os

class PDFReportGenerator:
    """Generate professional medical PDF reports"""
    
    def __init__(self, output_dir=None):
        """
        Initialize PDF generator
        
        Args:
            output_dir: Directory to store generated PDFs (defaults to project root/reports/generated_reports)
        """
        if output_dir is None:
            # Use project root/reports/generated_reports as default
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            output_dir = os.path.join(project_root, 'reports', 'generated_reports')
        
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_pdf(self, report_data, image_path=None):
        """
        Generate professional PDF from report data
        
        Args:
            report_data: Dictionary containing report information
            image_path: Path to retinal image to include in PDF
        
        Returns:
            str: Path to generated PDF file
        """
        # Generate filename
        filename = f"{report_data['report_id']}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                              topMargin=0.5*inch,
                              bottomMargin=0.5*inch,
                              leftMargin=0.75*inch,
                              rightMargin=0.75*inch)
        
        # Build story (content)
        story = []
        styles = getSampleStyleSheet()

        label_style = ParagraphStyle(
            'LabelStyle',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Bold',
            leading=12
        )

        value_style = ParagraphStyle(
            'ValueStyle',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            leading=12
        )
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=6,
            alignment=1,  # Center
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("DIABETIC RETINOPATHY SCREENING REPORT", title_style))
        story.append(Paragraph(f"<font size=10 color='#666666'>Automated AI-Assisted Diagnosis System</font>", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Facility Header
        facility_style = ParagraphStyle(
            'FacilityStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1f4788'),
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(report_data['screening']['facility'], facility_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Two-column layout for patient info with proper alignment
        patient_data = report_data['patient']
        screening_data = report_data['screening']
        
        # Create structured patient info with labels and values
        patient_label_style = ParagraphStyle(
            'PatientLabel',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1f4788'),
            leading=14
        )
        
        patient_value_style = ParagraphStyle(
            'PatientValue',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            leading=14
        )
        
        patient_table_data = [
            [
                Paragraph("Patient Name:", patient_label_style),
                Paragraph(f"{patient_data['name']}", patient_value_style),
                Paragraph("Report ID:", patient_label_style),
                Paragraph(f"{report_data['report_id']}", patient_value_style)
            ],
            [
                Paragraph("Patient ID:", patient_label_style),
                Paragraph(f"{patient_data['id']}", patient_value_style),
                Paragraph("Report Date:", patient_label_style),
                Paragraph(f"{report_data['report_date']}", patient_value_style)
            ],
            [
                Paragraph("Age:", patient_label_style),
                Paragraph(f"{patient_data['age']} years", patient_value_style),
                Paragraph("Physician:", patient_label_style),
                Paragraph(f"{screening_data['physician']}", patient_value_style)
            ],
            [
                Paragraph("Gender:", patient_label_style),
                Paragraph(f"{patient_data['gender']}", patient_value_style),
                Paragraph("Modality:", patient_label_style),
                Paragraph(f"{screening_data['imaging_modality']}", patient_value_style)
            ]
        ]
        
        # Equal column widths for better alignment
        patient_table = Table(patient_table_data, colWidths=[1.2*inch, 1.8*inch, 1.5*inch, 2.0*inch])
        patient_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.HexColor('#d0d0d0')),
        ]))
        
        story.append(patient_table)
        story.append(Spacer(1, 0.25*inch))
        
        # Clinical Findings Section
        findings_style = ParagraphStyle(
            'SectionHead',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.white,
            backColor=colors.HexColor('#1f4788'),
            spaceAfter=6,
            fontName='Helvetica-Bold',
            leftIndent=5,
            rightIndent=5
        )
        
        story.append(Paragraph("CLINICAL FINDINGS", findings_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Findings details with better alignment
        findings = report_data['findings']
        severity_colors = {
            "Low": "#00AA00",
            "Moderate": "#FFAA00",
            "High": "#FF6600",
            "Very High": "#FF3300",
            "Critical": "#CC0000"
        }
        
        risk_color = severity_colors.get(findings['risk_level'], "#000000")
        
        findings_label_style = ParagraphStyle(
            'FindingsLabel',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1f4788'),
            leading=14
        )
        
        findings_value_style = ParagraphStyle(
            'FindingsValue',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            leading=14
        )
        
        findings_table_data = [
            [
                Paragraph("Classification", findings_label_style),
                Paragraph(f"<font color='{risk_color}'><b>{findings['classification']}</b></font>", findings_value_style)
            ],
            [
                Paragraph("Risk Level", findings_label_style),
                Paragraph(f"<font color='{risk_color}'><b>{findings['risk_level']}</b></font>", findings_value_style)
            ],
            [
                Paragraph("Model Confidence", findings_label_style),
                Paragraph(f"{findings['confidence']}", findings_value_style)
            ],
            [
                Paragraph("Image Analyzed", findings_label_style),
                Paragraph(f"{findings['image_analyzed']}", findings_value_style)
            ]
        ]
        
        # Better column proportioning for findings
        findings_table = Table(findings_table_data, colWidths=[1.8*inch, 4.7*inch])
        findings_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(findings_table)
        story.append(Spacer(1, 0.25*inch))
        
        # Clinical Assessment
        story.append(Paragraph("CLINICAL ASSESSMENT", findings_style))
        story.append(Spacer(1, 0.12*inch))
        
        assessment_style = ParagraphStyle(
            'Assessment',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            alignment=4,  # Justified
            leftIndent=8,
            rightIndent=8
        )
        story.append(Paragraph(report_data['clinical_assessment'], assessment_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Recommendations
        story.append(Paragraph("CLINICAL RECOMMENDATIONS", findings_style))
        story.append(Spacer(1, 0.12*inch))
        recommendation_text = f"<b>Recommendation:</b> {report_data['recommendations']}"
        story.append(Paragraph(recommendation_text, assessment_style))
        story.append(Spacer(1, 0.25*inch))
        
        # Next Steps
        story.append(Paragraph("NEXT STEPS", findings_style))
        story.append(Spacer(1, 0.08*inch))

        step_style = ParagraphStyle(
            'StepStyle',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            leftIndent=15,
            rightIndent=8
        )
        
        for idx, step in enumerate(report_data['next_steps'], 1):
            story.append(Paragraph(f"<b>{idx}.</b> {step}", step_style))
            story.append(Spacer(1, 0.08*inch))

        story.append(Spacer(1, 0.25*inch))
        
        # Footer with disclaimers
        story.append(Spacer(1, 0.15*inch))
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#666666'),
            leading=11,
            leftIndent=5,
            rightIndent=5,
            alignment=4  # Justified
        )
        
        disclaimer_text = f"""
        <b>⚠️ IMPORTANT DISCLAIMER:</b><br/>
        {report_data['disclaimer']}<br/><br/>
        <b>Data Protection:</b> This medical record is confidential and intended only for the named patient and authorized healthcare providers.<br/>
        """
        
        story.append(Paragraph(disclaimer_text, footer_style))
        
        # Build PDF
        doc.build(story)
        
        return filepath


def create_pdf_report(report_data, image_path=None, output_dir=None):
    """
    Convenience function to create PDF report
    
    Args:
        report_data: Dictionary with report information
        image_path: Optional path to retinal image
        output_dir: Directory to save PDF (defaults to project root/reports/generated_reports)
    
    Returns:
        str: Path to generated PDF file
    """
    generator = PDFReportGenerator(output_dir=output_dir)
    return generator.generate_pdf(report_data, image_path)
