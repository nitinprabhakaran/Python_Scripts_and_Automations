import pandas as pd

def split_ip_ranges(df):
    # Function to split IP ranges into separate rows
    def split_row(row):
        ip_range = row['ip']
        if '_' in ip_range:
            ips = ip_range.split('_')
            # Create a new DataFrame for each IP
            rows = [row.copy() for _ in ips]
            for r, ip in zip(rows, ips):
                r['ip'] = ip
            return pd.DataFrame(rows)
        else:
            return pd.DataFrame([row])

    # Apply the split_row function to each row and concatenate the results
    split_df = pd.concat(df.apply(split_row, axis=1).values, ignore_index=True)
    return split_df

# Example usage
data = {
    'ip': ['10.172.2.5', '192.168.1.1_192.168.1.10_192.168.1.20', '10.0.0.1'],
    'value': [1, 2, 3]
}
df = pd.DataFrame(data)
split_df = split_ip_ranges(df)
print(split_df)