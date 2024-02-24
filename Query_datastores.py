from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch
from tabulate import tabulate

def create_pdf_with_tables(file_name, tables):
    # Create a PDF document
    pdf = SimpleDocTemplate(file_name, pagesize=letter)
    story = []

    # Add black rectangle shape to canvas for background color
    black_rect = Table([[('',)]], colWidths=[pdf.width], rowHeights=[pdf.height])
    black_rect.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.black)]))
    story.append(black_rect)

    # Generate tables and add them to the PDF
    for table_data in tables:
        # Create table object
        table = Table(table_data["data"], colWidths=[100] * len(table_data["headers"]))

        # Define table style
        style = TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),  # Set text color to white
            ('BACKGROUND', (0, 0), (-1, -1), colors.black), # Set background color to black
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TEXTCOLOR', (2, 1), (2, -1), colors.green),  # Set font color for "Compliant" column to green
            ('TEXTCOLOR', (2, 1), (2, -1), colors.red)     # Set font color for "Non-Compliant" column to red
        ])

        # Apply style to table
        table.setStyle(style)

        # Add table to story
        story.append(table)
        story.append(Spacer(1, 12))

    # Build PDF
    pdf.build(story)

# Example usage
tables = [
    {
        "headers": ["Name", "Age", "Compliance"],
        "data": [
            ["John", 30, "Compliant"],
            ["Alice", 25, "Non-Compliant"],
            ["Bob", 35, "Compliant"]
        ]
    }
]

create_pdf_with_tables("tables_with_compliance.pdf", tables)