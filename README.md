# AeroGate USB

## Overview

AeroGate USB is an advanced digital forensic tool designed to enhance the efficiency, accuracy, and reliability of forensic investigations. Leveraging the capabilities of the Raspberry Pi 0 W and the P4wnP1 ALOA platform, AeroGate USB provides wireless, automated, and real-time data extraction and management. This project aims to address the limitations of traditional forensic tools by offering a portable, versatile, and user-friendly solution for forensic analysts.

## Features

- **Portable Design**: Compact and lightweight, AeroGate USB can be easily deployed in various environments, including office setups and field operations.
- **Remote Data Extraction**: Utilize wireless technologies to remotely extract data from targeted devices without physical access.
- **Real-Time Data Management**: A web server for centralized data storage, real-time monitoring, and data analysis.
- **Custom Forensic Payloads**: Automate key forensic tasks with custom scripts designed for various data extraction needs.
- **User-Friendly Interface**: Intuitive web interface for easy navigation and data management.
- **High Performance**: Efficient data extraction, low transmission latency, and high system throughput.

## Getting Started

### Prerequisites

- Raspberry Pi 0 W
- MicroSD Card (16GB or higher)
- USB Connector
- Power Supply (Micro-USB charger)
- Internet connection for network setup

### Installation

1. **Setup Raspberry Pi 0 W**:
   - Flash the Raspberry Pi OS onto the microSD card.
   - Connect the Raspberry Pi 0 W to power and internet.
   - Install the P4wnP1 ALOA platform on the Raspberry Pi 0 W.

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/YourUsername/AeroGate-USB.git
   cd AeroGate-USB

## Usage
Plug AeroGate USB into the Target Machine:

- Connect the AeroGate USB device to the target machine from which data will be extracted.

Connect Devices to Network:

- Ensure the target machine, server machine, and your smartphone or computer are connected to the same network.

Select and Run Payloads:

- Access the AeroGate USB interface via your smartphone or computer.

- Select the desired forensic payload and execute it on the target machine.

Manage and Analyze Data:

- Use the web server interface to manage, analyze, and download the extracted data.

## Scripts
### Connect Server Script
Starts the HTTP server on the Raspberry Pi, enabling remote access to forensic data.

### Cookie Extraction Script
Extracts cookie data from Google Chrome profiles on the target device.

### File Extraction Script
Automates the extraction of various file types from the target device.

### History Extraction Script
Retrieves browser history files from Google Chrome profiles.

### Logs Extraction Script
Exports system, security, and application event logs from the target device.

### Open Ports Script
Identifies active TCP and UDP connections on the target device.

### Running Processes & Services Script
Captures a list of running processes and the status of services on the target device.

### SAM & SYSTEM Extraction Script
Extracts the SAM and SYSTEM registry hives from the target device.

### USB Formatting Script
Formats the USB drive by deleting non-essential files.





### Acknowledgments
Special thanks to Dr. Haitham Ghalwash and Eng. May Shalaby for their guidance and support throughout this project. Thanks also to the forensic analysts and cybersecurity professionals who provided valuable feedback and insights during development and testing.

Contact
For any questions or further information, please contact:

Waleed Hesham Ibrahim
Email: waleed.mhmd.ibr@gmail.com
