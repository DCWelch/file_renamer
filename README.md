# [File Renamer](https://dcwelch.github.io/fr)

This File Renamer is a tool designed to rename a collection of vacation photos from various sources in a very simple, consistent, and specific way. The new naming format is primarily based on the date taken, when available, and can be represented as follows:
   ```bash
   <year>_<month>_<day>_<hour>_<id>
   ```
Examples:
   ```bash
   20230228_092122(0).png  -->  2023_02_28_09_001.png
   Snapchat-286861347.jpg  -->  2023_03_02_17_002.jpg
   Screenshot_20240620_124449_Chrome.jpg  -->  2024_06_20_12_003.jpg
   0 Travel Day (3aaa).heic  -->  2024_06_20_17_004.heic
   0 Travel Day (4).mp4  -->  2024_06_20_17_005.mp4
   ```

This tool was created for a very specific use case, so it is intentionally static and simple. Visit [dcwelch.github.io/fr](https://dcwelch.github.io/fr) for more high-level information.

![example_file_renamer_gui](https://github.com/user-attachments/assets/fcdd43af-fcf1-448f-b83b-66fc174a3122)

## Features
- Renames files using date taken-equivelant metadata (e.g., `DateTimeOriginal` for images)
- Handles missing metadata gracefully with fallback timestamps (typically using last modified date)
  - Designates these files in a separate, reviewable category prefixed with "ZZZ_"
- Support for a majority of common image and videos file formats, including...
  - .png/.jpg/.jpeg image files via `pillow`
  - .heic image files via `pillow-heif`
  - .mp4/.mov video files via `ffprobe`
  - no other file formats are currently tested, but most others should process normally using the fallback date at a minimum
- Logs operations which maintain name mapping to...
  1. A live GUI log window
  2. A log file in the selected directory and a dedicated `logs` directory
- Intuitive GUI built with `Tkinter`

## Alternatives

Many similar tasks may find themselves better solved with one of these tools:
- [Bulk Rename Utility](https://www.bulkrenameutility.co.uk/)
- [Microsoft PowerRename](https://learn.microsoft.com/en-us/windows/powertoys/powerrename)

## Download the latest version of the tool
Visit [dcwelch.github.io/fr](https://dcwelch.github.io/fr) or the repo's [Releases](https://github.com/DCWelch/file_renamer/releases) tab to download the executable and necessary supporting files, which are packaged together in a zip file called `rename_files_executable.zip`.

## Build the project from source
### Prerequisites
- Python 3.12 or later
- The following Python dependencies (included in `requirements.txt`):
  ```plaintext
  pillow
  pillow-heif
  pytz
  ```
- FFmpeg for `ffprobe` support (ensure it’s in your system PATH)
- pyinstaller (only if a new executable is desired)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/DCWelch/file_renamer.git
   cd file_renamer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python rename_files.py
   ```

### Build an Executable
To create a standalone executable:
1. Install `pyinstaller`:
   ```bash
   pip install pyinstaller
   ```
2. Use the following command to generate the executable:
   ```bash
   pyinstaller --noconfirm --noconsole --icon=file_renamer_icon.ico --add-data "file_renamer_icon.ico;." --hidden-import=pillow_heif --hidden-import=pytz.zoneinfo --exclude-module numpy --exclude-module mkl --exclude-module tcl --exclude-module tbb --exclude-module pywin32 --exclude-module psutil rename_files.py
   ```
3. The executable will be located in the `dist/` folder

## Usage
1. Launch the application (via rename_files.exe)
2. Use the `Pick Folder` button to select a target directory
3. Click `Start Renaming` to rename all files in the selected directory

## Directory Structure
```plaintext
file_renamer/
├── rename_files.py  # Main script
├── requirements.txt  # Dependencies
├── file_renamer_icon.ico  # App icon
├── .gitignore  # Specifies intentionally untracked files to ignore
├── LICENSE  # License
├── README.md  # Documentation
├── .github/  # Outlines GitHub Actions workflow for the build
│   └──
├── dist/  # Contains built executable (after running PyInstaller)
│   └── rename_files/
│       ├── rename_files.exe  # Executable file to launch the file_renamer GUI
│       └── _internal/  # Contains necessary dependencies for the executable
│           ├── logs/  # Stores log files (created at runtime)
│           │   └──
│           └──
└── build/  # Contains build artifacts (after running PyInstaller)
    └── 
```

## Contributing and Feedback

Contributions and feedback are always welcome! Here's how you can get involved:

### Reporting Issues or Requesting Features
If you encounter a bug or have ideas for new features, please use the [GitHub Issues](https://github.com/DCWelch/file_renamer/issues) page to...
- **Report Bugs**: Provide a clear description, steps to reproduce, and any relevant logs or screenshots
- **Request Features**: Share your suggestions for new features or improvements

### Submitting Code Contributions
If you'd like to contribute code changes...
1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Submit a pull request with a detailed description of your proposed changes

Any feedback, suggestions, or contributions are greatly appreciated!

## License
This project is licensed under the [MIT License](LICENSE)

## Acknowledgments
- **[`Pillow`](https://pillow.readthedocs.io/)**: For image processing and EXIF metadata handling
- **[`pillow-heif`](https://github.com/carsales/pillow-heif)**: For HEIC/HEIF image support
- **[`pytz`](https://pytz.sourceforge.net/)**: For timezone handling
- **[`FFmpeg`](https://ffmpeg.org/)**: For video metadata extraction via `ffprobe`
- **[`Tkinter`](https://docs.python.org/3/library/tkinter.html)**: For the graphical user interface
- **[`Flaticon`](https://www.flaticon.com/)**: [Folder icons](https://www.flaticon.com/free-icons/folder) created by [Freepik](https://www.flaticon.com/authors/freepik)
- The Python community: For providing the libraries and tools that power this application

## Contact
For questions, feedback, or support, feel free to contact me at [dcwelch545@gmail.com](mailto:dcwelch545@gmail.com)
