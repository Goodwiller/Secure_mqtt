# Result Evaluation Metric 2 (REM2): Time required by
# the broker to establish a connection to a client. (Averaged out for 100 iterations)

# Run the broker and record all the logs
# Connect all the clients to this broker (optional)
# Run REM1 for one of the clients
# Paste all the logs to ecord_logs.txt
# Run this file


import re

# Path to your saved log file
log_file_path = "broker_logs.txt"

# Regex patterns
conn_pattern = re.compile(r"New Connection acquired from\s+[\d\.]+ \d+ at\s+(\d+\.\d+)")
enc_pattern = re.compile(r"Encryption of permakey done.*?at\s+(\d+\.\d+)")

def analyze_logs():
    try:
        with open(log_file_path, "r") as f:
            log_data = f.read()

        # Extract timestamps
        connection_times = conn_pattern.findall(log_data)
        encryption_times = enc_pattern.findall(log_data)

        if len(connection_times) <= 1:
            print("⚠️ Not enough connections to analyze.")
            return

        # Ignore first connection
        connection_times = connection_times[1:]
        encryption_times = encryption_times[:len(connection_times)]

        print("\n📊 Connection Latency Report")
        latencies = []
        for i, (conn, enc) in enumerate(zip(connection_times, encryption_times)):
            latency = float(enc) - float(conn)
            latencies.append(latency)
            print(f"Connection {i+1}: {latency:.6f} seconds")

        print("\n--- Summary ---")
        print(f"Total connections analyzed: {len(latencies)}")
        print(f"Average latency: {sum(latencies)/len(latencies):.6f} seconds")

    except Exception as e:
        print(f"❌ Error during log analysis: {e}")

if __name__ == "__main__":
    analyze_logs()