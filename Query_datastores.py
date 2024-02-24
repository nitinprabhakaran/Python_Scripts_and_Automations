from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def create_pdf_with_tables(file_name, tables):
    # Create a PDF document
    pdf = SimpleDocTemplate(file_name, pagesize=letter)
    story = []

    # Generate tables and add them to the PDF
    for table_data in tables:
        # Create table object
        table = Table(table_data["data"], colWidths=[100] * len(table_data["headers"]))

        # Define table style
        style = TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),  # Set text color to white
            ('BACKGROUND', (0, 0), (-1, -1), colors.black), # Set background color to black
        ])

        # Apply style to table
        table.setStyle(style)

        # Add table to story
        story.append(table)

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