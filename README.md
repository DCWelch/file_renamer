# File Renaming Tool

## Overview
The File Renaming Tool is a user-friendly utility designed to rename files in a specified directory based on their metadata, such as the date they were taken or created. It supports images, videos, and various other file types, offering robust handling of metadata and fallback strategies.

## Features
- Renames files using metadata (e.g., `DateTimeOriginal` for images).
- Supports HEIC/HEIF formats via `pillow-heif`.
- Processes video files using `ffprobe`.
- Logs operations to:
  1. A live GUI log window.
  2. A log file in the target directory.
  3. A log file in a dedicated `logs` directory.
- Intuitive GUI built with `Tkinter`.
- Handles missing metadata gracefully with fallback timestamps.

## Installation
### Prerequisites
- Python 3.12 or later.
- The following Python dependencies (included in `requirements.txt`):
  ```plaintext
  pillow
  pillow-heif
  pytz
  ```
- FFmpeg for `ffprobe` support (ensure it’s in your system PATH).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python rename_files.py
   ```

## Usage
1. Launch the application.
2. Use the `Pick Folder` button to select the target directory.
3. Click `Start Renaming` to process files.
4. Logs will be displayed in the GUI, saved to the target directory, and stored in the `logs` folder.

## Build an Executable
To create a standalone executable:
1. Install `pyinstaller`:
   ```bash
   pip install pyinstaller
   ```
2. Use the following command to generate the executable:
   ```bash
   pyinstaller --noconfirm --noconsole --icon=file_renamer_icon.ico --add-data "file_renamer_icon.ico;." --hidden-import=pillow_heif --hidden-import=pytz.zoneinfo --exclude-module numpy --exclude-module mkl --exclude-module tcl --exclude-module tbb --exclude-module pywin32 --exclude-module psutil rename_files.py
   ```
3. The executable will be located in the `dist/` folder.

## Directory Structure
```plaintext
file_renamer/
├── rename_files.py  # Main script
├── requirements.txt  # Dependencies
├── file_renamer_icon.ico  # App icon
├── .gitignore  # Specifies intentionally untracked files to ignore
├── .github/  # Outlines GitHub Actions workflow for the build
├── logs/  # Stores log files (created at runtime)
├── dist/  # Contains built executable (after running PyInstaller)
│   └── rename_files/
│       ├── rename_files.exe  # Executable file to launch the file_renamer GUI
│       └── _internal/  # Contains necessary dependencies for the executable
├── build/  # Contains build artifacts (after running PyInstaller)
└── README.md  # Documentation
```

## Contributing
Contributions are welcome! Please...
1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Submit a pull request with a description of your proposed changes

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
- `pillow-heif` for HEIC/HEIF support
- `pytz` for timezone handling
- FFmpeg for video metadata processing
- [Folder icons](https://www.flaticon.com/free-icons/folder) created by [Freepik](https://www.flaticon.com/authors/freepik) - [Flaticon](https://www.flaticon.com).

## Contact
For questions or feedback, please reach out to [dcwelch545@gmail.com]
