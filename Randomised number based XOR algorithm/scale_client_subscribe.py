import subprocess
import signal
import os
import sys
import time

# Path to the script you want to run in each terminal
script_path = "C:/Users/iamra/Desktop/Secure_mqtt/secure_mqtt_using_xor_operations/client_subscribe.py"  # Adjust as needed
n = 15  # Number of terminals to spawn

# Store subprocess handles
processes = []

def spawn_terminals(n, script_path):
    print(f"🚀 Spawning {n} terminals running {script_path}...")

    for i in range(n):
        try:
            # Spawn a new terminal and run the script
            proc = subprocess.Popen(["start", "cmd", "/k", "python", script_path], shell=True)
            processes.append(proc)
            time.sleep(0.2)  # Optional: stagger launches
        except Exception as e:
            print(f"❌ Failed to launch terminal {i+1}: {e}")

    print("✅ All terminals launched. Press Ctrl+C to terminate them.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt received. Terminating all terminals...")
        for proc in processes:
            try:
                os.kill(proc.pid, signal.SIGTERM)
            except Exception as e:
                print(f"⚠️ Failed to terminate process {proc.pid}: {e}")
        print("✅ All terminals terminated.")
        sys.exit(0)

if __name__ == "__main__":
    spawn_terminals(n, script_path)