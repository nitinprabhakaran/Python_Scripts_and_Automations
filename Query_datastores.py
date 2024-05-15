from pysudoers import parse
from pysudoers.exceptions import ParseError

# Function to parse sudoers file and filter entries for a specific user
def parse_sudoers_and_filter(input_file, output_file, username):
    try:
        # Parse sudoers file
        with open(input_file, 'r') as f:
            sudoers_data = f.read()
        sudoers_entries = parse(sudoers_data)

        # Filter entries for specific user
        filtered_entries = [entry for entry in sudoers_entries if username in entry.users]

        # Write filtered entries to output file
        with open(output_file, 'w') as f:
            for entry in filtered_entries:
                f.write(str(entry) + '\n')

        print(f"Filtered sudoers entries for user {username} written to {output_file}")
    except FileNotFoundError:
        print("Input file not found.")
    except ParseError as e:
        print(f"Error parsing sudoers file: {e}")

# Example usage
input_file = 'sudoers'
output_file = 'filtered_sudoers'
username = 'example_user'

# Parse sudoers file and filter entries for the specified user
parse_sudoers_and_filter(input_file, output_file, username)