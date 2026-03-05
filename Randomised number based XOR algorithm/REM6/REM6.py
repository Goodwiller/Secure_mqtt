# Result Evaluation Metric 6 (REM6): Time required by
# the existing subscriber of a topic to recalculate the new
# group key when a new client subscribes to the topic. (already n subscribers are present)

# Run the broker as normal
# Connect all n-2 clients as usual
# Do the experiment with the n-a th client
# Log all the prints of the n-1 th cleint
# Ignore Ist rekey as it is for the n-1th client itself
# Run REM3 for 100 times
# Collect the logs in logs.txt
# The run this file.


import re

# Path to your saved log file
log_file_path = "logs.txt"

# Number of initial entries to ignore
n_skip = 1  # Change this to skip more or fewer entries

# Regex patterns
conn_pattern = re.compile(r"Rekey computation started at:\s+(\d+\.\d+)")
enc_pattern = re.compile(r"Rekey computation ended at:\s+(\d+\.\d+)")

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
