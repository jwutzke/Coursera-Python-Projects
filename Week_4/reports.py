"""Module for basic PDF generation.

This module provides the basics needed to generate a PDF and output to a
specific location on the filesystem.
"""
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate(filename, title, body):
    """Generate a PDF."""
    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(filename)
    report_title = Paragraph(title, styles["h1"])
    report_info = Paragraph(body, styles["BodyText"])
    empty_line = Spacer(1, 20)
    report.build([report_title, empty_line, report_info])
