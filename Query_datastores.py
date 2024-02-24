import streamlit as st
import pandas as pd
import time

# Function to perform animated checks
def perform_checks(data):
    checks = ["Check 1", "Check 2", "Check 3", "Check 4", "Check 5"]
    results = []

    for check in checks:
        # Simulate processing time for animation
        time.sleep(1)

        # Perform checks (example: check if dataframe is empty)
        if data.empty:
            result = "Failed"
        else:
            result = "Passed"

        # Append result
        results.append(result)

    return results

# Main function to run the Streamlit app
def main():
    # Title and file upload
    st.title("CSV Data Checker")
    st.sidebar.title("File Upload")
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file
        data = pd.read_csv(uploaded_file)

        # Display CSV data
        st.subheader("Uploaded Data")
        st.write(data)

        # Perform checks
        st.subheader("Performing checks...")
        with st.spinner("Performing checks..."):
            results = perform_checks(data)

        # Display results in table
        st.subheader("Check Results")
        results_df = pd.DataFrame({"Check": ["Check 1", "Check 2", "Check 3", "Check 4", "Check 5"],
                                   "Result": results})
        st.table(results_df)

# Run the Streamlit app
if __name__ == "__main__":
    main()