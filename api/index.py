from flask import Flask, render_template, jsonify
import speedtest
import re

app = Flask(__name__)

def extract_server_name(host):
    # Extract the server name from the host using a regular expression
    match = re.match(r'^.*\((.*)\).*$', host)
    if match:
        return match.group(1)
    else:
        return host

def run_speedtest():
    st = speedtest.Speedtest()

    # Get public IP address
    ip_address = st.get_best_server()['host']

    # Perform download speed test
    download_speed = st.download() / 1_000_000  # Convert to Mbps

    # Get server details
    server_details = st.get_best_server()

    # Extract server name from the host
    server_name = extract_server_name(server_details['host'])

    # Perform upload speed test only if download is successful
    if download_speed > 0:
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    else:
        upload_speed = 0

    result = {
        'ip_address': ip_address,
        'server': server_name,
        'host': server_details['host'],
        'latency': server_details['latency'],
        'ping_ms': server_details['latency'],
        'download_speed': round(download_speed, 2),
        'upload_speed': round(upload_speed, 2)
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False)
