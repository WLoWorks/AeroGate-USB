# AeroGate USB

## Overview

AeroGate USB is an advanced digital forensic tool designed to enhance the efficiency, accuracy, and reliability of forensic investigations.

## Features

- **Portable Design**: Compact and lightweight.
- **Remote Data Extraction**: Utilize wireless technologies.
- **Real-Time Data Management**: Web server for centralized data storage.

## Getting Started

### Prerequisites

- Raspberry Pi 0 W
- MicroSD Card
- USB Connector
- Power Supply

### Installation

1. **Setup Raspberry Pi 0 W**:
   - Flash the Raspberry Pi OS onto the microSD card.
   - Connect the Raspberry Pi 0 W to power and internet.
   - Install the P4wnP1 ALOA platform.

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/YourUsername/AeroGate-USB.git
   cd AeroGate-USB


Install required Python packages:
pip install -r requirements.txt
Ensure all necessary libraries for P4wnP1 ALOA are installed.


Start the web server using the provided script:
python3 http-server.py


Plug AeroGate USB into the Target Machine:
  Connect the AeroGate USB device to the target machine from which data will be extracted.

Connect Devices to Network:
  Ensure the target machine, server machine, and your smartphone or computer are connected to the same network.

Select and Run Payloads:
  Access the AeroGate USB interface via your smartphone or computer.
  Select the desired forensic payload and execute it on the target machine.

Manage and Analyze Data:
  Use the web server interface to manage, analyze, and download the extracted data.

Scripts:
Connect Server Script
  Starts the HTTP server on the Raspberry Pi, enabling remote access to forensic data.

Cookie Extraction Script
  Extracts cookie data from Google Chrome profiles on the target device.

File Extraction Script
  Automates the extraction of various file types from the target device.

History Extraction Script:
Retrieves browser history files from Google Chrome profiles.

Logs Extraction Script:
Exports system, security, and application event logs from the target device.

Open Ports Script:
  Identifies active TCP and UDP connections on the target device.

Running Processes & Services Script:
  Captures a list of running processes and the status of services on the target device.

SAM & SYSTEM Extraction Script:
  Extracts the SAM and SYSTEM registry hives from the target device.

USB Formatting Script:
  Formats the USB drive by deleting non-essential files.


Acknowledgments
Special thanks to Dr. Haitham Ghalwash and Eng. May Shalaby for their guidance and support throughout this project. Thanks to the forensic analysts and cybersecurity professionals who provided valuable feedback and insights during development and testing.

Contact
For any questions or further information, please contact:

Waleed Hesham Ibrahim
Email: waleed.mhmd.ibr@gmail.com
