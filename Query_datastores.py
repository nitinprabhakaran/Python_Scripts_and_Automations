import streamlit as st
import pandas as pd
import time
from PIL import Image
import io

# Function to perform animated checks
def perform_checks(data):
    checks = ["Check 1", "Check 2", "Check 3", "Check 4", "Check 5"]
    results = []

    for check in checks:
        # Simulate processing time for animation
        time.sleep(1)

        # Perform checks (example: check if dataframe is empty)
        if data.empty:
            result = "<span style='color:red; font-weight:bold;'>Failed</span>"
        else:
            result = "<span style='color:green; font-weight:bold;'>Passed</span>"

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

        # Download button for image
        if st.button("Download Table as Image"):
            # Convert DataFrame to HTML
            table_html = results_df.to_html(index=False, escape=False)

            # Capture HTML table as image
            img_bytes = st._server.capture_html(table_html)
            table_img = Image.open(io.BytesIO(img_bytes))

            # Save image
            image_path = "table_image.png"
            table_img.save(image_path)
            st.success(f"Table image saved as {image_path}")

# Run the Streamlit app
if __name__ == "__main__":
    main()