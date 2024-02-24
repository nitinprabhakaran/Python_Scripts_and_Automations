from prettytable import PrettyTable

def prettytable_to_markdown(table):
    # Extract header and data
    header = table.field_names
    data = table._rows
    
    # Convert header to Markdown format
    markdown_table = "| " + " | ".join(header) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(header)) + " |\n"
    
    # Convert data to Markdown format
    for row in data:
        markdown_table += "| " + " | ".join(str(cell) for cell in row) + " |\n"
    
    return markdown_table

def write_prettytable_to_md(file_name, table):
    # Convert PrettyTable to Markdown format
    markdown_table = prettytable_to_markdown(table)
    
    # Write Markdown content to file
    with open(file_name, "w") as f:
        f.write(markdown_table)

# Example usage
table = PrettyTable()
table.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
table.add_row(["Adelaide", 1295, 1158259, 600.5])
table.add_row(["Brisbane", 5905, 1857594, 1146.4])
table.add_row(["Darwin", 112, 120900, 1714.7])
table.add_row(["Hobart", 1357, 205556, 619.5])

write_prettytable_to_md("table.md", table)