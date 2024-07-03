import pandas as pd

def split_ip_ranges(df):
    # Function to split IP ranges into separate rows
    def split_row(row):
        ip_range = row['ip']
        if '_' in ip_range:
            start_ip, end_ip = ip_range.split('_')
            row1 = row.copy()
            row2 = row.copy()
            row1['ip'] = start_ip
            row2['ip'] = end_ip
            return pd.DataFrame([row1, row2])
        else:
            return pd.DataFrame([row])

    # Apply the split_row function to each row and concatenate the results
    split_df = pd.concat(df.apply(split_row, axis=1).values, ignore_index=True)
    return split_df

# Example usage
data = {
    'ip': ['10.172.2.5', '192.168.1.1_192.168.1.10', '10.0.0.1'],
    'value': [1, 2, 3]
}
df = pd.DataFrame(data)
split_df = split_ip_ranges(df)
print(split_df)