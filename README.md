# Folder Monitoring and run sample Script

This repository contains a Python script to monitor a directory for changes in the number of subfolders and trigger a face encoding script (`encode_faces.py`) when a change is detected. The script integrates with a PostgreSQL database to store and retrieve folder counts.

## Features

- **Subfolder Monitoring**: Counts the number of subfolders in a specified directory.
- **Database Integration**: Uses PostgreSQL to persist and retrieve the global folder count.
- **Trigger External Script**: Automatically runs `encode_faces.py` upon detecting changes in the directory.

## Prerequisites

- Python 3.6+
- PostgreSQL database
- `psycopg2` library for database connection

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install required Python libraries:
   ```bash
   pip install psycopg2
   ```

3. Set up the PostgreSQL database:
   - Create a database (e.g., `folder_monitor_db`).
   - Create a table:
     ```sql
     CREATE TABLE folder_monitor (
         id SERIAL PRIMARY KEY,
         global_file_count INT NOT NULL,
         folder_length INT NOT NULL
     );
     ```
   - Insert an initial row:
     ```sql
     INSERT INTO folder_monitor (global_file_count, folder_length) VALUES (0, 0);
     ```

4. Update the database connection details in the script (`dbname`, `user`, `password`, `host`, `port`).

## Usage

1. Place the `encode_faces.py` script in the same directory as this script or provide the correct path.
2. Run the script:
   ```bash
   python folder_monitor.py
   ```
3. The script will:
   - Retrieve the global file count from the database.
   - Count the current number of subfolders in the `dataset` directory.
   - Trigger `encode_faces.py` if there are changes.
   - Update the database with the new counts.

## Configuration

- **Dataset Directory**: The directory to monitor is set as `dataset` in the script. Update this if needed.
- **Database Configuration**: Modify the following placeholders in the script:
  ```python
  dbname="your_database_name",
  user="your_username",
  password="your_password",
  host="your_host",
  port="your_port"
  ```

## Notes

- Ensure the `dataset` directory exists before running the script.
- If you are monitoring a different folder, update the `dataset_path` variable in the script.
- The `encode_faces.py` script must be functional and accessible to the monitoring script.

## Future Improvements

- Add logging for better traceability.
- Extend support for monitoring multiple directories.
- Implement error notifications.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

