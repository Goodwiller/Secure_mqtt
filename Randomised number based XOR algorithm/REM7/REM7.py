# Result Evaluation Metric 7 (REM7): Time required by
# the existing subscriber of a topic to recalculate the new
# group key when an existing client unsubscribes to the
# topic.

# start the broker in normal mode
# Connect 3 clients to the broker in normal mode
# use 4th node to take readings
# Run REM7 code 100 times and unsubscribe each time.
# Ignore fisrt 2 rekey events (1 for 4th clinet 1 for 5 the client joining)
# After that take the first rekey in each cycle


import re

# Path to your log file
log_file_path = "logs.txt"

# Number of initial rekey groups to skip
n_skip = 2  # Change this as needed

# Regex patterns
start_pattern = re.compile(r"Rekey computation started at:\s+(\d+\.\d+)")
end_pattern = re.compile(r"Rekey computation ended at:\s+(\d+\.\d+)")

def analyze_logs():
    try:
        with open(log_file_path, "r") as f:
            log_data = f.read()

        # Extract all start and end timestamps
        start_times = start_pattern.findall(log_data)
        end_times = end_pattern.findall(log_data)

        # Group into rekey pairs
        rekey_pairs = list(zip(start_times, end_times))

        if len(rekey_pairs) <= n_skip:
            print(f"⚠️ Not enough rekey groups to analyze after skipping first {n_skip}.")
            return

        # Skip first n rekey groups
        rekey_pairs = rekey_pairs[n_skip:]

        print(f"\n📊 Alternate Rekey Latency Report (skipping first {n_skip} groups)")
        latencies = []
        for i, (start, end) in enumerate(rekey_pairs):
            if i % 2 == 0:  # Every alternate entry
                latency = float(end) - float(start)
                latencies.append(latency)
                print(f"Rekey Group {i + n_skip + 1}: {latency:.6f} seconds")

        print("\n--- Summary ---")
        print(f"Total alternate rekey groups analyzed: {len(latencies)}")
        print(f"Average latency: {sum(latencies)/len(latencies):.6f} seconds")

    except Exception as e:
        print(f"❌ Error during log analysis: {e}")

if __name__ == "__main__":
    analyze_logs()