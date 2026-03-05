# Result Evaluation Metric 8 (REM8): Time required by
# the broker to recalculate the challenge that has to be
# broadcast to recalculate the new group key when an
# existing client unsubscribes to the topic.

# run the broker as normal
# connect all n-1 clients as normal
# Run REM7_client for nth client
#   copy the logs
#  run this file

import re

# Path to your log file
log_file_path = "logs.txt"

# Regex patterns
start_pattern = re.compile(r"Rekey computation started at\s+(\d+\.\d+)")
end_pattern = re.compile(r"Rekey computation ended for client at\s+(\d+\.\d+)")

def analyze_logs():
    try:
        with open(log_file_path, "r") as f:
            log_data = f.read()

        # Extract timestamps
        start_times = start_pattern.findall(log_data)
        end_times = end_pattern.findall(log_data)

        # Pair and compute latencies
        rekey_pairs = list(zip(start_times, end_times))
        latencies = []

        print("\n📊 Rekey Computation Latency Report")
        for i, (start, end) in enumerate(rekey_pairs):
            latency = float(end) - float(start)
            latencies.append(latency)
            print(f"Rekey {i+1}: {latency:.6f} seconds")

        # Summary
        print("\n--- Summary ---")
        print(f"Total rekey events analyzed: {len(latencies)}")
        print(f"Average latency: {sum(latencies)/len(latencies):.6f} seconds")

    except Exception as e:
        print(f"❌ Error during log analysis: {e}")

if __name__ == "__main__":
    analyze_logs()