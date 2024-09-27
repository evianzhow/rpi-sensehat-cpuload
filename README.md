# SenseHAT CPU Load Visualizer on Raspberry Pi

This project displays real-time CPU load on an 8x8 SenseHAT LED matrix connected to a Raspberry Pi. The CPU load is updated every 10 seconds, and the last bar animates smoothly, creating a visual representation of system performance.

## Features
- **CPU Load Monitoring**: Fetches CPU load every 10 seconds and displays it as vertical bars on the SenseHAT.
- **Smooth Animation**: The last CPU load bar gradually animates from 0 to its full value for better visual effect.
- **System-Level Daemon**: The script can be set up to run as a daemon using `systemd`.

## Requirements

1. Raspberry Pi with SenseHAT
2. Python 3.x
3. Required Python libraries: 
   - `psutil` for fetching CPU load
   - `sense-hat` for interacting with the SenseHAT

You can install the necessary libraries using pip:
```bash
sudo pip install psutil sense-hat
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/evianzhow/rpi-sensehat-cpuload.git
cd rpi-sensehat-cpuload
```

### 2. Make the Script Executable
Make the main Python script executable by running:
```bash
sudo chmod +x /path/to/the/main.py
```

### 3. Setup Systemd Service

A `systemd` service is provided to run the script as a background service.

1. Copy the `python-daemon.service` file to `/etc/systemd/system/`:
    ```bash
    sudo cp python-daemon.service /etc/systemd/system/
    ```

2. Reload systemd daemon to recognize the new service:
    ```bash
    sudo systemctl daemon-reload
    ```

3. Start the service:
    ```bash
    sudo systemctl start python-daemon
    ```

4. Enable the service to start on boot:
    ```bash
    sudo systemctl enable python-daemon
    ```

Now, the CPU load visualizer will run in the background as a system-level service, and it will automatically start after a reboot.

## Usage

Once the service is running, the SenseHAT will display real-time CPU load with a smooth animated effect for the last bar.

### Manually Start/Stop the Service
You can manage the service using `systemctl`:
```bash
# Stop the service
sudo systemctl stop python-daemon

# Restart the service
sudo systemctl restart python-daemon

# Check the service status
sudo systemctl status python-daemon
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
