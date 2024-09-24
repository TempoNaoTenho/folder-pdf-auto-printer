PDF Auto Printer
This project is a Python script designed to monitor a folder for newly added or modified PDF files and automatically print them using SumatraPDF. The script runs in the background, allowing continuous monitoring while handling printing tasks on a separate thread.

Features
Folder Monitoring: Monitors a designated folder for any new or modified PDF files.
Automatic Printing: Automatically sends detected PDF files to the default printer via SumatraPDF.
Multithreading: Uses a separate thread to handle printing tasks without blocking the folder monitoring.
File Stability Check: Ensures that files are stable and completely downloaded before printing (e.g., handling temporary files like .crdownload and .part).
Configurable Folder Path: Offers the option to use a default or custom folder for monitoring.
Prerequisites
Before running the script, you need the following:

Python 3.x
SumatraPDF installed and configured to print to the default printer.
Watchdog Python package for monitoring file system events:

bash
pip install watchdog
Python Dotenv for loading environment variables:
bash

pip install python-dotenv
A .env file in the root directory of the project to configure the following variables:
SUMATRA_PATH: Path to the SumatraPDF executable (e.g., C:/Program Files/SumatraPDF/SumatraPDF.exe)
DEF_MONITORING_FOLDER: Default folder path to be monitored (e.g., C:/PDFs)
Installation
Clone the repository:

bash
git clone https://github.com/yourusername/pdf-auto-printer.git
cd pdf-auto-printer
Create a .env file in the root directory of the project with the following content:

ini
SUMATRA_PATH="C:/Program Files/SumatraPDF/SumatraPDF.exe"
DEF_MONITORING_FOLDER="C:/PDFs"

Install the required dependencies:

bash
pip install -r requirements.txt

Usage
To start monitoring a folder for PDF files and printing them automatically:

Run the script:

bash
python main.py
When prompted, choose the type of folder monitoring:

Press 1 to use the default folder path defined in the .env file.
Press 2 to specify a custom folder path.
The script will then start monitoring the chosen folder. Any new or modified PDF files will be automatically sent to the default printer using SumatraPDF.

Example

yaml
Choose the type of monitoring:
1 - Default folder monitoring : C:/PDFs
2 - Custom folder monitoring
--------------------------------------------------

Option: 1
Monitoring folder: C:/PDFs
Once a PDF file is detected, the output will show:

arduino
PDF file ready for printing: example.pdf
Sending file example.pdf to the printer...
Stopping the Script
Press Ctrl + C to stop the script and terminate the monitoring process.

Customization
You can modify the default folder path and SumatraPDF executable path by editing the .env file:

ini
SUMATRA_PATH="C:/Path/To/SumatraPDF/SumatraPDF.exe"
DEF_MONITORING_FOLDER="C:/Path/To/Monitor"
Troubleshooting
Ensure that SumatraPDF is installed and accessible from the path provided in the .env file.
If the script doesn't detect PDF files, verify that the folder path is correct and check for any file permission issues.
Use the log messages printed by the script to debug any issues during file processing or printing.
Contributions
Contributions, issues, and feature requests are welcome! Feel free to open a pull request or submit an issue in the issues page.

License
This project is licensed under the MIT License. See the LICENSE file for details.

This README provides clear installation and usage instructions, explains the features and purpose of the script, and encourages contributions. You can modify the repository URLs, author details, or adjust the description based on your preferences.