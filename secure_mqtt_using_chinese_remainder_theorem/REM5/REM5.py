# Result Evaluation Metric 5 (REM5): Time required
# by the broker to process a subscription request from
# a new client for a topic with n existing member.


# Run the broker and record all the logs
# Connect all the n clients to this broker
# change the value of n_skip
# Run REM3.py for one of the clients
# Paste all the logs to record_logs.txt
# Run this file


import re

# Path to your saved log file
log_file_path = "broker_logs.txt"

# Number of initial entries to ignore
n_skip = 15  # Change this to skip more or fewer entries

# Regex patterns
conn_pattern = re.compile(r"Subscription computation started for client at\s+(\d+\.\d+)")
enc_pattern = re.compile(r"Subscription computation ended at\s+(\d+\.\d+)")

def analyze_logs():
    try:
        with open(log_file_path, "r") as f:
            log_data = f.read()

        # Extract timestamps
        connection_times = conn_pattern.findall(log_data)
        encryption_times = enc_pattern.findall(log_data)

        if len(connection_times) <= n_skip:
            print(f"⚠️ Not enough connections to analyze after skipping first {n_skip}.")
            return

        # Skip first n entries
        connection_times = connection_times[n_skip:]
        encryption_times = encryption_times[n_skip:len(connection_times) + n_skip]

        print(f"\n📊 Connection Latency Report (skipping first {n_skip} entries)")
        latencies = []
        for i, (conn, enc) in enumerate(zip(connection_times, encryption_times)):
            latency = float(enc) - float(conn)
            latencies.append(latency)
            print(f"Connection {i+1 + n_skip}: {latency:.6f} seconds")

        print("\n--- Summary ---")
        print(f"Total connections analyzed: {len(latencies)}")
        print(f"Average latency: {sum(latencies)/len(latencies):.6f} seconds")

    except Exception as e:
        print(f"❌ Error during log analysis: {e}")

if __name__ == "__main__":
    analyze_logs()