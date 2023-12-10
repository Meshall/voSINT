![Logo](Results/logo.png)
# voSINT: Video Reverse Search OSINT Tool

## Description
voSINT is an Open Source Intelligence (OSINT) tool designed for video reverse search. It enables users to trace the digital footprint of a video across the internet. By listing the results in descending order, voSINT reveals where a video first appeared and its subsequent occurrences online. This tool is invaluable for cybersecurity experts, digital forensics analysts, and anyone interested in the origin and spread of digital content.

Key Features:
- Track video appearances online in descending order.
- Generate approximate results, prioritizing data scope.
- Beta version focused on user feedback and continuous improvement.

## Installation Guide
Navigate to the directory where you want to create your project.

### Setting up a Virtual Environment
Run the following command to create a virtual environment (replace 'venv' with your desired environment name):
```bash
python3 -m venv venv
```
Activate the virtual environment:
```bash
source venv/bin/activate
```
Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage Instructions
For using the tool with a single video:
```bash
python voSINT.py <video_path>
```
For multiple videos in a directory:
```bash
python voSINT.py <videos_dir>
```

By creating and activating a virtual environment, you ensure that the installed packages and dependencies are isolated from your system's global Python environment, providing a clean and separate environment for your project.
