"""Prints PDF files added to a folder using SumatraPDF.

This script monitors a folder for new PDF files and prints them using
SumatraPDF. It runs in the background and can be stopped by pressing
Ctrl+C.

The script uses a queue to store the files to be printed and a separate
thread to print the files. This allows the script to continue running
and monitoring the folder while the files are being printed.

Obviusly, this script requires SumatraPDF to be installed and configured to print
to the default printer.

"""
import os
import sys
import time
import queue
import subprocess
import threading

from pathlib import Path

from dotenv import load_dotenv
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

load_dotenv()
SUMATRA_PATH = f"{os.getenv('SUMATRA_PATH')}"
DEF_MONITORING_FOLDER = f"{os.getenv("DEF_MONITORING_FOLDER")}"

class PDFHandler(FileSystemEventHandler):
    """Handles file creation and modification events for PDF files.

    Attributes:
        processed_files (dict): Stores the timestamps of processed files.
        print_queue (queue.Queue): The queue where the files to be printed are
        placed.

    """

    def __init__(self, print_queue: queue.Queue) -> None:
        """Initialize the PDFHandler class and storage processed files timestamps."""
        self.processed_files = {}
        self.print_queue = print_queue

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        self._process_event(event)

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        self._process_event(event)

    def _process_event(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        # .crdownload/.part = temporary files created by browsers
        monitored_extensions = [".pdf", ".crdownload", ".part"]
        file_path = Path(os.fsdecode(event.src_path))
        file_extension = file_path.suffix.lower()

        if file_extension not in monitored_extensions:
            return

        # Wait untill the file is stable
        stable = False
        while not stable:
            try:
                initial_size = file_path.stat().st_size
                time.sleep(1)
                new_size = file_path.stat().st_size
                if initial_size == new_size:
                    stable = True
                else:
                    continue
            except FileNotFoundError:
                return

        # Verify if the file is a PDF
        if file_path.suffix.lower() != ".pdf":
            # Verify if the file suffix is renamed to .pdf
            possible_pdf = file_path.with_suffix(".pdf")
            if possible_pdf.exists():
                file_path = possible_pdf
            return # Not a PDF

        # Gets the timestamp of the file last modification
        last_modified = file_path.stat().st_mtime

        # Verify if the file has already been processed based on the timestamp
        processed_timestamp = self.processed_files.get(str(file_path))

        if processed_timestamp == last_modified:
            return # Already processed
        self.processed_files[str(file_path)] = last_modified

        print(f"Arquivo PDF pronto para impressão: {file_path.name}")

        # Add the file to the print queue
        self.print_queue.put(file_path)


def print_worker(print_queue: queue.Queue) -> None:
    """Run in a separate thread and prints PDF files in the print queue.

    This function runs an infinite loop and checks if there are files in the
    print queue. If there are, it tries to print the file using SumatraPDF. If
    there are not, it waits until a file is added to the queue. If the file is
    printed successfully, the task is marked as done with `task_done()`. If an
    error occurs, the error is printed to the standard output and the task is
    marked as done with `task_done()`. The thread is stopped when the value
    `None` is added to the print queue.
    """
    while True:
        file_path = print_queue.get()
        if file_path is None:
            # Break the loop when `None` is added to the queue
            break
        try:
            # Path to the SumatraPDF executable (check if it's correct)
            if not SUMATRA_PATH:
                e_msg = "The path to the SumatraPDF executable was not found."
                raise FileNotFoundError(e_msg) #noqa: TRY301

            sumatra_pdf_path = Path(SUMATRA_PATH)

            # Check if the executable exists
            if not sumatra_pdf_path.exists():
                e_msg = "The SumatraPDF executable was not found at"
                e_msg += f"{sumatra_pdf_path}"
                raise FileNotFoundError(e_msg) #noqa: TRY301

            # Silently printer and close afterwards
            print(f"Enviando o arquivo {file_path.name} para a impressora...")
            subprocess.call([str(sumatra_pdf_path), #noqa: S603
                             "-print-to-default",
                             "-silent", str(file_path)])

        except Exception as e: #noqa: BLE001
            print(f"Erro ao enviar para a impressora: {e}")
        finally:
            print_queue.task_done()


def monitorar_pasta(folder_path: Path, print_queue: queue.Queue) -> None:
    """Start monitoring a folder for PDF files.

    # Parameters:

    folder_path : Path
        Path to the folder to be monitored.
    print_queue : queue.Queue
        Print queue where the PDF files should be added.

    # Notes:

    The function runs an infinite loop and checks if there are PDF files in the
    folder. If there are, it adds the file to the print queue. If an error
    occurs, the error is printed to the standard output and the task is marked
    as done with `task_done()`. The thread is stopped when the value `None` is
    added to the print queue.
    """
    event_handler = PDFHandler(print_queue)
    observer = Observer()
    observer.schedule(event_handler, str(folder_path), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def iniciar_monitoramento_em_thread(folder_path: Path,
                                    print_queue: queue.Queue) -> None:
    """Start monitoring in a separate thread.

    # Parameters:
        folder_path : Path
            Path to the folder to be monitored.
        print_queue : queue.Queue
            Print queue where the files to be printed will be added.
    """
    monitor_thread = threading.Thread(target=monitorar_pasta,
                                      args=(folder_path, print_queue))
    # Defines a thread as daemon to finalize with the main program
    monitor_thread.daemon = True
    monitor_thread.start()


if __name__ == "__main__":
    input_value = input(f"""Choose the type of monitoring:
                            1 - Default folder monitoring : {DEF_MONITORING_FOLDER}
                            2 - Custom folder monitoring
                            --------------------------------------------------
                            Option: """)
    if input_value == "1":
        folder_path = Path(DEF_MONITORING_FOLDER).resolve()
    elif input_value == "2":
        folder_path_input = input("Custom folder path (eg. C:/PDFs): ")
        folder_path = Path(folder_path_input).resolve()
        try:
            # Check if the folder exists
            if not folder_path.exists():
                error_msg = f"Folder {folder_path} not exists."
                raise Exception(error_msg) # noqa: TRY301, TRY002
        except Exception as e: # noqa: BLE001
            print(e)
            sys.exit()
    else:
        msg = "Invalid input. Please enter 1 or 2."
        raise ValueError(msg)

    if input_value in ["1", "2"]:
        print(f"Monitoring folder: {folder_path}")
        # Create file queue
        print_queue = queue.Queue()
        # Initialize the print worker thread
        print_worker_thread = threading.Thread(target=print_worker,
                                               args=(print_queue,))
        print_worker_thread.daemon = True
        print_worker_thread.start()
        # Start monitoring in a separately thread
        iniciar_monitoramento_em_thread(folder_path, print_queue)

    try:
        while True:
            # keep the program alive while the thread is running
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        # Send None to the print queue to stop the worker thread
        print_queue.put(None)
        print_worker_thread.join()
