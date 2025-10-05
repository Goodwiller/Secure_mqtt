import subprocess
import re

# Path to your client_subscribe.py
script_path = "C:/Users/iamra/Desktop/Secure_mqtt/secure_mqtt_using_chinese_remainder_theorem/REM7_client_subscribe.py"

# Regex patterns
start_pattern = re.compile(r"Subscription process with network latency started at:\s+(\d+\.\d+)")
end_pattern = re.compile(r"Subscription process with network latency ended at:\s+(\d+\.\d+)")

latencies = []

for i in range(100):
    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout

        start_match = start_pattern.search(output)
        end_match = end_pattern.search(output)

        if start_match and end_match:
            start_time = float(start_match.group(1))
            end_time = float(end_match.group(1))
            latency = end_time - start_time
            latencies.append(latency)
            print(f"Run {i+1}: Latency = {latency:.6f} seconds")
        else:
            print(f"Run {i+1}: Failed to extract latency timestamps")

    except subprocess.CalledProcessError as e:
        print(f"Run {i+1}: Script error\n{e.stderr}")

# Summary
print("\n--- Summary ---")
print(f"Total successful runs: {len(latencies)}")
if latencies:
    print(f"Average latency: {sum(latencies)/len(latencies):.6f} seconds")