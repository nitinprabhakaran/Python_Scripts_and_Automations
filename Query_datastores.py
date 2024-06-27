import pandas as pd

def process_dataframe(input_file, iteration=1):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Define the column name
    column_name = 'baseImageNameTagValue'
    
    if column_name in df.columns:
        # Check if all values in the column are blank
        if df[column_name].str.strip().eq('').all():
            print("All values in the column are blank. No action needed.")
        else:
            # Generate the new column name
            new_column_name = f"{column_name}{iteration}"
            
            # Rename the column
            df.rename(columns={column_name: new_column_name}, inplace=True)
            
            # Save the modified DataFrame to a new CSV file
            output_file = f"output_{iteration}.csv"
            df.to_csv(output_file, index=False)
            
            print(f"Column renamed to '{new_column_name}' and saved to '{output_file}'")
            
            # Recursively call the function with incremented iteration
            process_dataframe(output_file, iteration + 1)
    else:
        print(f"Column '{column_name}' does not exist in the DataFrame.")

# Define the input CSV file name
input_file = 'input.csv'

# Process the DataFrame
process_dataframe(input_file)