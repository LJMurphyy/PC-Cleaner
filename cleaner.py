import shutil

class DownloadsCleaner:
    _source = ""

    _new_directories = [
        "Documents", "Images", "Videos", 
        "Audio", "Archive", "Code", "System",
        "Applications"
        ]
    
    _categories = {
        "System": [".exe", ".bat", ".sh", ".cmd", ".sys", ".dll", ".ini", ".log", ".conf", ".cfg"],
        "Code": [".py", ".js", ".java", ".c", ".cpp", ".h", ".cs", ".html", ".css", ".rb", ".php", ".r", ".json", ".xml", ".yml", ".yaml", ".jar"],
        "Archive": [".zip", ".rar", ".7z", ".gz", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".xz"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
        "Videos": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm", ".mov", ".MOV"],
        "Images": [".jpg", ".JPG", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".svg", ".ico", ".img", ".heic", ".HEIC"],
        "Documents": [".csv", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".rtf", ".odt", ".ods", ".odp"],
        "Applications": [".app", ".dmg"]
    }

    def __init__(self, source):
        self._source = source

    def set_directories(self):
        for directory in self._new_directories:
                directory_path = self._source / directory
                directory_path.mkdir(parents=True, exist_ok=True)

    def clean_directory(self):
        try:
            for file_path in self._source.iterdir():
                file_extension = file_path.suffix
                self.move_file(file_path, file_extension)

        except FileNotFoundError as e:
            print(f"File error: {e}")
        except PermissionError as e:
            print(f"Permission error: {e}")
        except Exception as e:
            print(f"An unexpected error: {e}")

    def move_file(self, file_path, file_extension):
        for category, extensions, in self._categories.items():            
            if file_extension in extensions:
                destination = self._source / category / file_path.name
                shutil.move(file_path, destination)