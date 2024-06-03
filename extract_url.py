import re
import argparse

def extract_url_from_log(log_line):
    try:
        # Extract request field
        request_field_match = re.search(r'request="(.*?)"', log_line)
        if not request_field_match:
            print("No request field found in log line")
            return None
        request_field = request_field_match.group(1)

        # Debugging: print the extracted request field
        #print(f"Extracted request field: {request_field}")

        # Extract the protocol from the log line
        protocol_match = re.search(r'protocol="(.*?)"', log_line)
        if not protocol_match:
            print("No protocol field found in log line")
            return None, None
        protocol = protocol_match.group(1).strip().lower()

        # Debugging: print the extracted protocol
        #print(f"Extracted protocol: {protocol}")

        # Extract the host from the request field
        host_match = re.search(r'Host: ([:a-zA-Z0-9.-]+)', request_field)
        if not host_match:
            print("No host found in request field")
            return None
        host = host_match.group(1).strip()

        # Debugging: print the extracted host
        #print(f"Extracted host: {host}")

        # Extract the path from the request field
        path_match = re.search(r'(GET|POST|OPTIONS|PUT|DELETE|HEAD|PATCH|TRACE|CONNECT) (.*?) HTTP', request_field)
        if not path_match:
            print("No path found in request field")
            return None
        path = path_match.group(2).strip()
        method = path_match.group(1).strip()

        # Debugging: print the extracted path
        #print(f"Extracted path: {path}")

        # Form the URL without the protocol prefix
        url = f"{method} {protocol}://{host}{path}"
        return url
    except Exception as e:
        print(f"Error processing log line: {e}")
        return None

parser = argparse.ArgumentParser(description='Parse URL from the app-protect security log file')
parser.add_argument("log_file", help="Path to app-protect security log file")
args = parser.parse_args()
log_file_path = args.log_file

try:
    with open(log_file_path, 'r') as file:
        for line in file:
            #print(f"Processing line: {line.strip()}")
            url = extract_url_from_log(line)
            if url:
                print(f"Extracted URL: {url}")
            else:
                print("No URL extracted")
except FileNotFoundError:
    print(f"Log file not found: {log_file_path}")
except Exception as e:
    print(f"Error reading log file: {e}")
