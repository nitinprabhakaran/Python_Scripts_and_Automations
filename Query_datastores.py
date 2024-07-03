import pandas as pd
import ipaddress

def ip_in_range(ip, ip_range):
    start_ip, end_ip = ip_range.split('_')
    return ipaddress.IPv4Address(start_ip) <= ipaddress.IPv4Address(ip) <= ipaddress.IPv4Address(end_ip)

def lookup_ip_addresses(input_ips, input_csv, output_csv):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)

    def matches(ip, row_ip):
        if '_' in row_ip:
            return ip_in_range(ip, row_ip)
        else:
            return ip == row_ip

    # Filter the DataFrame for exact IP address matches or IP ranges
    filtered_df = df[df['ip'].apply(lambda row_ip: any(matches(ip, row_ip) for ip in input_ips))]

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_csv, index=False)

# Example usage
input_ips = ['10.172.2.5', '192.168.1.1']
input_csv = 'input.csv'
output_csv = 'output.csv'
lookup_ip_addresses(input_ips, input_csv, output_csv)