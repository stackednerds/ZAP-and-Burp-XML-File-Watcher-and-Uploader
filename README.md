# ZAP and Burp XML File Watcher and Uploader

This Python script watches a directory for new OWASP ZAP or Burp Suite XML reports and uploads them to the DefectDojo API. If no new XML files are detected within a set time, the script stops.

## How It Works

1. **Watches a Directory**: The script monitors a specified folder for new XML files (e.g., OWASP ZAP or Burp Suite reports).
2. **Uploads Existing Files**: When started, the script first checks for any existing XML files in the directory and uploads them.
3. **Uploads New Files**: When a new XML file is detected, it uploads the file to the DefectDojo API.
4. **Deletes Files**: After successful upload, the XML file is deleted from the directory.
5. **Timeout**: If no new files are detected within a given time, the script stops.

## Configuration

- **TOKEN**: Your DefectDojo API token.
- **PRODUCT_NAME**: Name of the product in DefectDojo.
- **ENGAGEMENT_NAME**: Name of the engagement in DefectDojo.
- **DIRECTORY_TO_WATCH**: The folder to watch for new XML files.
- **TIMEOUT**: Time in seconds before the script stops if no new files are detected.
- **URL**: The base URL for the DefectDojo API.

## Requirements

- Python 3.x
- Install the required libraries using:
  ```sh
  pip install requests watchdog
  ```

## Running the Script

To run the script, execute:
```sh
python watcher.py
```

## Example Usage

1. Set up the folder you want to monitor (e.g., `./my_security_reports`).
2. Place your XML reports (e.g., OWASP ZAP or Burp Suite XML files) in this folder.
3. The script will:
   - Check for existing XML files in the folder and upload them one by one.
   - Detect new XML files in the folder and upload them.
   - Delete the files from the folder after a successful upload.
   - If no new files are found within the timeout period, the script will stop.

## Notes

- Ensure your DefectDojo API token is set correctly in the script.
- The script will print messages to indicate its status.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*Current Date and Time (UTC)*: 2025-02-26 12:39:24
*Current User's Login*: DUMBANIKET
