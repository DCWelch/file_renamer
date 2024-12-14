import os
import datetime
from tkinter import Tk, Label, Button, filedialog, Text, Scrollbar, END, RIGHT, Y, BOTH, LEFT, BOTTOM, Frame
from PIL import Image
from PIL.ExifTags import TAGS
import mimetypes
import subprocess
from pytz import timezone
import sys
from pillow_heif import register_heif_opener

eastern = timezone('US/Eastern')

progress_steps = [
    "Waiting...",
    "Launching...",
    "Finding Files...",
    "Extracting Dates...",
    "Sorting Files...",
    "Renaming Files...",
    "Output Statistics...",
    "Complete..."
]

LOG_FILE_NAME = "file_rename_log.txt"

register_heif_opener()

def write_log(message):
    log_widget.insert(END, message + "\n")
    log_widget.see(END)
    log_widget.update()
    with open(main_log_file, "a") as log_file:
        log_file.write(message + "\n")
    with open(secondary_log_file, "a") as log_file:
        log_file.write(message + "\n")

def update_progress_bar(current_step):
    for idx, step_label in enumerate(progress_bar_labels):
        if idx == current_step:
            step_label.config(bg="lightgreen", fg="black")
        elif idx < current_step:
            step_label.config(bg="gray", fg="white")
        else:
            step_label.config(bg="lightgray", fg="black")
    progress_bar.update()

def generate_log_filename(base_name, directory):
    """
    Generate a unique log filename in the given directory.
    """
    filename = f"{base_name}.txt"
    counter = 2
    while os.path.exists(os.path.join(directory, filename)):
        filename = f"{base_name}_{counter}.txt"
        counter += 1
    return os.path.join(directory, filename)

def get_date_taken(file_path):
    fallback_creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
    fallback_modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    date_taken = None
    is_fallback = True

    try:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and mime_type.startswith('image'):
            image = Image.open(file_path)

            if mime_type in ("image/heic", "image/heif"):
                try:
                    try:
                        import piexif
                    except ImportError as e:
                        write_log(f"[ERROR] Failed to import piexif: {e}")
    
                    metadata = image.info.get("exif")
                    xmp_data = image.info.get("xmp")

                    if metadata:
                        try:
                            exif_dict = piexif.load(metadata)
                            
                            datetime_original = exif_dict.get("Exif", {}).get(piexif.ExifIFD.DateTimeOriginal)
                            if datetime_original:
                                datetime_original = datetime_original.decode("utf-8")  # Convert bytes to string
                                naive_time = datetime.datetime.strptime(datetime_original, '%Y:%m:%d %H:%M:%S')
                                date_taken = eastern.localize(naive_time) if naive_time.tzinfo is None else naive_time.astimezone(eastern)
                                is_fallback = False

                            if date_taken is None:
                                datetime_digitized = exif_dict.get("Exif", {}).get(piexif.ExifIFD.DateTimeDigitized)
                                if datetime_digitized:
                                    datetime_digitized = datetime_digitized.decode("utf-8")
                                    naive_time = datetime.datetime.strptime(datetime_digitized, '%Y:%m:%d %H:%M:%S')
                                    date_taken = eastern.localize(naive_time) if naive_time.tzinfo is None else naive_time.astimezone(eastern)
                                    is_fallback = False
                        except Exception as exif_error:
                            write_log(f"[ERROR] Failed to parse EXIF metadata using piexif for {file_path}: {exif_error}")

                    if date_taken is None and xmp_data:
                        try:
                            import xml.etree.ElementTree as ET
                            root = ET.fromstring(xmp_data)
                            create_date = root.find(".//{http://ns.adobe.com/xap/1.0/}CreateDate")
                            if create_date is not None:
                                naive_time = datetime.datetime.strptime(create_date.text, '%Y-%m-%dT%H:%M:%S')
                                date_taken = eastern.localize(naive_time) if naive_time.tzinfo is None else naive_time.astimezone(eastern)
                                is_fallback = False
                        except Exception as xmp_error:
                            write_log(f"[ERROR] Failed to parse XMP metadata for {file_path}: {xmp_error}")

                except Exception as e:
                    write_log(f"[ERROR] Processing HEIC/HEIF metadata failed for {file_path}: {e}")

            else:
                exif_data = image._getexif()
                if exif_data:
                    for tag, value in exif_data.items():
                        decoded = TAGS.get(tag, tag)
                        if decoded == "DateTimeOriginal":
                            naive_time = datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                            date_taken = eastern.localize(naive_time) if naive_time.tzinfo is None else naive_time.astimezone(eastern)
                            is_fallback = False
                            break
                        elif decoded == "DateTimeDigitized":
                            naive_time = datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                            date_taken = eastern.localize(naive_time) if naive_time.tzinfo is None else naive_time.astimezone(eastern)
                            is_fallback = False
                            break

        elif mime_type and mime_type.startswith('video'):
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                 "format_tags=creation_time", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )
            creation_time = result.stdout.decode().strip()
            if creation_time:
                naive_time = datetime.datetime.fromisoformat(creation_time.replace('Z', ''))
                date_taken = eastern.localize(naive_time) if naive_time.tzinfo is None else naive_time.astimezone(eastern)
                is_fallback = False

    except Exception as e:
        write_log(f"Error processing file {file_path}:  {e}")

    if date_taken is None:
        date_taken = eastern.localize(fallback_modification_time)

    return date_taken, is_fallback

def rename_files_by_date(folder_path):
    global main_log_file, secondary_log_file

    script_directory = os.path.dirname(os.path.abspath(__file__))
    logs_directory = os.path.join(script_directory, "logs")

    os.makedirs(logs_directory, exist_ok=True)

    main_log_file = generate_log_filename("file_rename_log", logs_directory)
    secondary_log_file = generate_log_filename("file_rename_log", folder_path)

    write_log("File Rename Log")
    write_log("=" * 40)
    write_log("")

    write_log("Step 1:  Launching rename script...")
    update_progress_bar(1)
    write_log(f"Timezone being used:  {eastern.zone}")

    write_log("Step 2:  Finding files in folder...")
    excluded_extensions = [".txt"]
    files = [
        os.path.normpath(os.path.join(folder_path, f)) 
        for f in os.listdir(folder_path) 
        if os.path.isfile(os.path.join(folder_path, f)) and not any(f.lower().endswith(ext) for ext in excluded_extensions)
    ]
    total_files = len(files)
    write_log(f"Found {total_files} files in folder:  {folder_path} (excluding .txt files)")

    write_log("Step 3:  Extracting dates from files...")
    update_progress_bar(3)
    padding_size = len(str(total_files))
    fallback_counter = 0
    file_dates = []

    for file in files:
        date_info = get_date_taken(file)
        date_taken, is_fallback = date_info if isinstance(date_info, tuple) else (None, True)

        fallback_creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file))
        fallback_modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file))

        if is_fallback:
            fallback_counter += 1

        file_dates.append((file, date_taken, is_fallback, fallback_creation_time, fallback_modification_time))

        if is_fallback:
            write_log(f"No Date Taken Found. Fallback Date Modified for {file}:  {date_taken} ({date_taken.strftime('%Y_%m_%d_%H')})" if date_taken else f"No Date Taken Found. Fallback failed for {file}. Defaulting to unknown date.")
            write_log(f"  Date Taken: N/A")
        else:
            write_log(f"Date Taken for {file}:  {date_taken} ({date_taken.strftime('%Y_%m_%d_%H')})")
            write_log(f"  Date Taken:  {date_taken}")

        write_log(f"  Creation:  {fallback_creation_time}")
        write_log(f"  Last Modified:  {fallback_modification_time}")

    write_log("Step 4:  Sorting files by date...")
    update_progress_bar(4)
    file_dates.sort(key=lambda x: x[1] or fallback_modification_time)  # Sort by date_taken or fallback
    write_log("Files sorted by date.")

    write_log("Step 5:  Renaming files...")
    update_progress_bar(5)
    for idx, (file_path, date, is_fallback, _, _) in enumerate(file_dates, start=1):
        if date is None:
            continue
        date_taken_year = str(date.year)
        date_taken_month = str(date.month).zfill(2)
        date_taken_day = str(date.day).zfill(2)
        date_taken_hour = str(date.hour).zfill(2)
        date_taken_id = str(idx).zfill(padding_size)
        prefix = "ZZZ_" if is_fallback else ""
        new_name = f"{prefix}{date_taken_year}_{date_taken_month}_{date_taken_day}_{date_taken_hour}_{date_taken_id}{os.path.splitext(file_path)[1]}"
        new_path = os.path.normpath(os.path.join(folder_path, new_name))
        try:
            os.rename(file_path, new_path)
            write_log(f"Renamed:  {file_path}  -->  {new_name}")
        except PermissionError as e:
            write_log(f"PermissionError:  {e} on file {file_path}")

    write_log("Renaming complete.")
    write_log("Step 6:  Output Statistics...")
    update_progress_bar(6)
    write_log(f"Total files processed:  {total_files}")
    write_log(f"...Of which, the number of files using a fallback timestamp:  {fallback_counter}")
    write_log("File Renaming Complete.")
    update_progress_bar(7)

def create_gui():

    global log_widget, progress_bar, progress_bar_labels

    def pick_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_label.config(text=f"Selected Folder: {folder}")
            rename_button.config(state="normal")

    def start_renaming():
        folder = folder_label.cget("text").replace("Selected Folder: ", "")
        if folder:
            log_widget.delete(1.0, END)
            rename_files_by_date(folder)

    root = Tk()
    root.title("File Renaming Tool")

    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, "file_renamer_icon.ico")
    else:
        icon_path = "file_renamer_icon.ico"
    root.iconbitmap(icon_path)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.75)
    window_height = int(screen_height * 0.75)

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=True)

    progress_bar = Frame(main_frame)
    progress_bar.pack(fill=BOTH, pady=5)
    progress_bar_labels = []
    for step in progress_steps:
        label = Label(progress_bar, text=step, width=15, padx=5, pady=5, bg="lightgray", fg="black", relief="solid", bd=1)
        label.pack(side=LEFT, fill=BOTH, expand=True)
        progress_bar_labels.append(label)

    folder_label = Label(main_frame, text="No Folder Selected", wraplength=400)
    folder_label.pack(pady=10)

    pick_folder_button = Button(main_frame, text="Pick Folder", command=pick_folder)
    pick_folder_button.pack(pady=5)

    rename_button = Button(main_frame, text="Start Renaming", state="disabled", command=start_renaming)
    rename_button.pack(pady=5)

    log_frame = Frame(main_frame)
    log_frame.pack(fill=BOTH, expand=True, pady=10)

    log_widget = Text(log_frame, wrap="word")
    log_widget.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(log_frame, command=log_widget.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    log_widget.config(yscrollcommand=scrollbar.set)

    quit_button = Button(root, text="Quit", command=root.quit)
    quit_button.pack(side=BOTTOM, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
