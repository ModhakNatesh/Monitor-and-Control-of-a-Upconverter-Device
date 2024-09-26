import socket
import threading
import time
import signal
from ping3 import ping
import sys
from django.core.cache import cache
from device_app.models import Device

# Device IP and Port
DEVICE_IP = '172.29.3.29'  # Actual IP
DEVICE_PORT = 54474  # Actual Port

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

lock = threading.Lock()

def send_command(command):
    try:
        sock.sendall(command.encode('utf-8') + b'\r\n')
        response = sock.recv(1024).decode('utf-8').strip()
        return response
    except Exception as e:
        print(f"Error sending command: {e}")
        return None

# 1. Control frequency (Set frequency)
def set_frequency(frequency):
    freq_str = f"{int(frequency):04d}"  
    command = f"*SFR:0{freq_str}000000"
    response = send_command(command)
    frequency = response.split(":")[1][1:5] if response else None
    print(f"Frequency set to: {frequency} MHz")
    return frequency

# 2. Control gain (Set gain)
def set_gain(gain):
        gain_value = int(gain)
        sign = "+" if gain >= 0 else "-"  # Determine the sign
        gain = abs(gain_value) 
        command = f"*SGA:{sign}{gain}"
        response = send_command(command)
        gain_response = response.split(":")[1].strip() if response else None
        print(f"Gain set to: {gain_response} dB")
        return gain_response

# 3. Control mute status (Set mute)
def set_mute(mute):
    command = f"*SMU:{mute}"
    response = send_command(command)
    mute_status = response.split(":")[1] if response else None
    print(f"Mute Status set to: {mute_status}")
    return mute_status

# 4. Control frequency step (Set frequency step)
def set_frequency_step(step):
    freq_step_str = f"{int(step):04d}"  # Format step as a 4-digit number with leading zeros
    command = f"*SFS:0{freq_step_str}000000"
    response = send_command(command)
    frequency_step = response.split(":")[1][3:5] if response else None
    print(f"Frequency Step set to: {frequency_step} Hz")
    return frequency_step

# Ensure to handle connection and disconnection
def connect_device():
    try:
        sock.connect((DEVICE_IP, DEVICE_PORT))
        print("Connected to the device")
        return True
    except Exception as e:
        print(f"Failed to connect: {e}")
        return False

def close_connection():
    try:
        sock.close()
        print("Connection closed")
    except Exception as e:
        print(f"Error closing connection: {e}")

def handle_exit(signal, frame):
    print("Shutting down...")
    close_connection()  # Close the connection on shutdown
    sys.exit(0)

def is_device_reachable(ip):
    # Use ping to check if the device is reachable
    response_time = ping(ip, timeout=5)
    return response_time is not None

# Monitoring functions
def get_frequency():
    command = "*GFR"
    response = send_command(command)
    frequency = response.split(":")[1][1:5] if response else None
    print(f"Frequency: {frequency} MHz")
    return frequency

def get_gain():
    command = "*GGA"
    response = send_command(command)
    gain = response.split(":")[1].strip() if response else None
    print(f"Gain: {gain} dB")
    return gain

def get_mute():
    command = "*GMU"
    response = send_command(command)
    mute_status = response.split(":")[1] if response else None
    print(f"Mute Status: {mute_status}")
    return mute_status

def get_frequency_step():
    command = "*GFS"
    response = send_command(command)
    frequency_step = response.split(":")[1][3:5] if response else None
    print(f"Frequency Step: {frequency_step} Hz")
    return frequency_step

def parse_status_response(response):
    if response:
        parts = response.split(":")[1].split(",")
        return {
            'error_status': parts[0].strip(),
            'control_status': parts[1].strip(),
            'output_frequency': parts[2].strip(),
            'data_source_freq': parts[3].strip(),
            'output_frequency_step': parts[4].strip(),
            'data_source_freq_step': parts[5].strip(),
            'gain': parts[6].strip(),
            'data_source_gain': parts[7].strip(),
            'mute_state': parts[8].strip(),
            'data_source_mute': parts[9].strip(),
            'reference_status': parts[10].strip(),
            'temperature': parts[11].strip(),
            'current_memory': parts[12].strip(),
        }
    return {}

def monitor_device():
    while True:
        with lock:  # Use the lock to ensure mutual exclusion
            # Fetch device parameters
            if not is_device_reachable(DEVICE_IP):
            # Device is not reachable, handle it
                cache.set('device_disconnected', True, timeout=60)  # Cache timeout in seconds
                break
            frequency = send_command("*GFR")
            gain = send_command("*GGA")
            mute = send_command("*GMU")
            frequency_step = send_command("*GFS")

            # Update or create the device entry in the database
            device, created = Device.objects.update_or_create(
                PK=1,
                defaults={
                    'frequency': frequency,
                    'gain': gain,
                    'mute': mute,
                    'frequency_step': frequency_step
                }
            )
            response = send_command("*ASK")
            status = parse_status_response(response)

            temperature = status.get('temperature')
            # Check for any changes and create alerts
            alerts = []
            
            if float(temperature) > 35:
                alerts.append(f"Temperature above threshold: {temperature}°C")
            
            # Store alerts in cache
            cache.set('device_alerts', alerts, timeout=60)  # Cache timeout in seconds
        
        time.sleep(5)  # Check every second


connection = connect_device()

if connection:
    # Start monitoring device in a background thread
    monitor_thread = threading.Thread(target=monitor_device, daemon=True)
    monitor_thread.start()


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)