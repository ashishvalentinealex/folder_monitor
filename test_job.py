#!/usr/bin/env python3

import os
import subprocess
import time
import logging

def count_subfolders(directory):
    """Counts the number of subfolders in the given directory."""
    return len([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))])

def read_global_file_count(file_path):
    """Reads the global file count from a .txt file."""
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("0")
        return 0
    try:
        with open(file_path, "r") as file:
            return int(file.read().strip())
    except ValueError:
        logging.warning("Invalid data in the file. Resetting to 0.")
        with open(file_path, "w") as file:
            file.write("0")
        return 0

def write_global_file_count(file_path, count):
    """Writes the global file count to a .txt file."""
    with open(file_path, "w") as file:
        file.write(str(count))

def main():
    # Configure logging to write to script_output.log
    logging.basicConfig(
        filename='/home/pipra/Desktop/final_demo/face_recognition/face_recognition_by_pi/script_output.log',
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Paths
    dataset_path = "/home/pipra/Desktop/final_demo/face_recognition/face_recognition_by_pi/database"
    global_count_file = "/home/pipra/Desktop/final_demo/face_recognition/face_recognition_by_pi/last_subfolder_count.txt"

    # Validate dataset path
    if not os.path.exists(dataset_path):
        logging.error(f"Error: The folder '{dataset_path}' does not exist.")
        return

    while True:
        try:
            # Read the global file count
            global_file_count = read_global_file_count(global_count_file)
            # Count the number of subfolders in the dataset
            folder_count = count_subfolders(dataset_path)

            logging.info(f"Global file count: {global_file_count}, Current folder count: {folder_count}")

            if folder_count != global_file_count:
                logging.info("Change detected. Running encode_faces.py...")

                # Run the script and wait for it to finish
                result = subprocess.run(
                    ["python", "/home/pipra/Desktop/final_demo/face_recognition/face_recognition_by_pi/02_encode_faces.py"],
                    capture_output=True,
                    text=True,
                    check=True
                )

                # Log the output (stdout and stderr)
                logging.info(f"encode_faces.py output: {result.stdout}")
                if result.stderr:
                    logging.error(f"encode_faces.py errors: {result.stderr}")

                # Update the global file count in the .txt file
                write_global_file_count(global_count_file, folder_count)
                logging.info("Global file count updated successfully.")
            else:
                logging.info("No changes detected.")

        except subprocess.CalledProcessError as e:
            logging.error(f"Error while running encode_faces.py: {e}")
            if e.stdout:
                logging.error(f"encode_faces.py output: {e.stdout}")
            if e.stderr:
                logging.error(f"encode_faces.py errors: {e.stderr}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

        # Wait for 1 minute before checking again
        time.sleep(60)

if __name__ == "__main__":
    main()

