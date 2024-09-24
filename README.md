# PDF Auto Printer

This project is a Python script designed to monitor a folder for newly added or modified PDF files and automatically print them using **SumatraPDF**. The script runs in the background, allowing continuous monitoring while handling printing tasks on a separate thread.

## Features

- **Folder Monitoring**: Monitors a designated folder for any new or modified PDF files.
- **Automatic Printing**: Automatically sends detected PDF files to the default printer via **SumatraPDF**.
- **Multithreading**: Uses a separate thread to handle printing tasks without blocking the folder monitoring.
- **File Stability Check**: Ensures that files are stable and completely downloaded before printing (e.g., handling temporary files like `.crdownload` and `.part`).
- **Configurable Folder Path**: Offers the option to use a default or custom folder for monitoring.

## Prerequisites

Before running the script, you need the following:

1. **Python 3.x**
2. **SumatraPDF** installed and configured to print to the default printer.
3. **Watchdog** Python package for monitoring file system events:
    ```bash
    pip install watchdog
    ```
4. **Python Dotenv** for loading environment variables:
    ```bash
    pip install python-dotenv
    ```
5. A `.env` file in the root directory of the project to configure the following variables:
    - `SUMATRA_PATH`: Path to the SumatraPDF executable (e.g., `C:/Program Files/SumatraPDF/SumatraPDF.exe`)
    - `DEF_MONITORING_FOLDER`: Default folder path to be monitored (e.g., `C:/PDFs`)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/pdf-auto-printer.git
    cd pdf-auto-printer
    ```

2. **Create a `.env` file** in the root directory of the project with the following content:
    ```ini
    SUMATRA_PATH="C:/Program Files/SumatraPDF/SumatraPDF.exe"
    DEF_MONITORING_FOLDER="C:/PDFs"
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start monitoring a folder for PDF files and printing them automatically:

1. Run the script:
    ```bash
    python main.py
    ```

2. When prompted, choose the type of folder monitoring:
    - Press `1` to use the default folder path defined in the `.env` file.
    - Press `2` to specify a custom folder path.

3. The script will then start monitoring the chosen folder. Any new or modified PDF files will be automatically sent to the default printer using **SumatraPDF**.

### Example

```bash
Choose the type of monitoring:
1 - Default folder monitoring : C:/PDFs
2 - Custom folder monitoring
--------------------------------------------------
Option: 1
Monitoring folder: C:/PDFs
```

Once a PDF file is detected, the output will show:
```bash
PDF file ready for printing: example.pdf
Sending file example.pdf to the printer...
```

## Stopping the Script
Press Ctrl + C to stop the script and terminate the monitoring process.

Customization
You can modify the default folder path and SumatraPDF executable path by editing the .env file:

```bash
SUMATRA_PATH="C:/Path/To/SumatraPDF/SumatraPDF.exe"
DEF_MONITORING_FOLDER="C:/Path/To/Monitor"
```

## Troubleshooting
    - Ensure that SumatraPDF is installed and accessible from the path provided in the .env file.
    - If the script doesn't detect PDF files, verify that the folder path is correct and check for any file permission issues.
    - Execute main.py (from environment) as administrator if necessary.

## License
This project is licensed under the MIT License. See the LICENSE file for details.




