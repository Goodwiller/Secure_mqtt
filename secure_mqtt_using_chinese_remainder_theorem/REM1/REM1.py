# Result Evaluation Metric 1 (REM1): Time required by
# client to establish a connection to the broker. (Averaged out for 100 iterations)

# Run the broker with normal settings
# Connect all clients to the broker (optional)
# Connect and disconnect this client 100 times and record the average value of time reqired. 

import subprocess
import re

# Path to your client_subscribe.py
script_path = "C:/Users/iamra/Desktop/Secure_mqtt/secure_mqtt_using_chinese_remainder_theorem/REM1_client_subscribe.py"

# Regex patterns to extract timestamps
start_pattern = re.compile(r"Connection process started at\s+(\d+\.\d+)")
end_pattern = re.compile(r"Connection process ended at\s+(\d+\.\d+)")

durations = []

for i in range(100):
    try:
        # Run the script and capture output
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout

        # Extract timestamps
        start_match = start_pattern.search(output)
        end_match = end_pattern.search(output)

        if start_match and end_match:
            start_time = float(start_match.group(1))
            end_time = float(end_match.group(1))
            duration = end_time - start_time
            durations.append(duration)
            print(f"Run {i+1}: Duration = {duration:.6f} seconds")
        else:
            print(f"Run {i+1}: Failed to extract timestamps")

    except subprocess.CalledProcessError as e:
        print(f"Run {i+1}: Script error\n{e.stderr}")

# Optional: Summary stats
print("\n--- Summary ---")
print(f"Total successful runs: {len(durations)}")
if durations:
    print(f"Average duration: {sum(durations)/len(durations):.6f} seconds")