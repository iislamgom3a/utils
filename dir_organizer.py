# --- This script works only on windows --- #
# --- Author: https://github.com/iislamgom3a ---# 

import os
import stat
import shutil

# --- ANSI Color Codes ---
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'


# source_dir
script_path = os.path.abspath(__file__)
source_dir = os.path.dirname(script_path)

# user profile (works only for windows)
user_prof = os.environ.get('USERPROFILE')

# windows dirs (Pictures, Documents, Music, Vidoes)
pics_dir =os.path.join(user_prof, "Pictures")
docs_dir =os.path.join(user_prof, "Documents")
aud_dir = os.path.join(user_prof, "Music")
vid_dir = os.path.join(user_prof, "Videos")

paths ={
    "Pictures":pics_dir, 
    "Documents": docs_dir,
    "Music": aud_dir, 
    "Videos": vid_dir, 
    "software" : os.path.join(source_dir, "software"), 
    "archives" : os.path.join(source_dir, "archives"),
    "src": os.path.join(source_dir, "src")
    
}
# creating additiondl dirs in the current dir  
# "src" stands for source code 
dirs = ["software",  "archives", "src"]
for i in dirs: 
    os.makedirs(os.path.join(source_dir, i), exist_ok=True)

source_dir_content = os.listdir(source_dir)

# checking if the file is hidden (the scirpt doesn't move the hidden file)
# works only for windows
def ishidden(path:str)->bool: 
    atrib = os.stat(path).st_file_attributes
    if atrib & stat.FILE_ATTRIBUTE_HIDDEN:
        return True 
    else :
        return False 

# define the extensions dic 
file_type_extensions = {
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".webm", ".mpeg", ".3gp", ".ts"],
    "Documents": ["",".pdf", ".one", ".odt", ".odf", ".xps", ".txt", ".rtf", ".tex", ".epub", ".chm", ".djvu", ".xls", ".xlsx", ".xlsm", ".xlt", ".xltx", ".csv", ".ods", ".ppt", ".pptx", ".pps", ".ppsx", ".pot", ".potx", ".odp", ".doc", ".docx", ".dot", ".dotx"],
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".heic", ".raw", ".svg"],
    "Music": [".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".opus", ".wma", ".alac", ".amr", ".aiff", ".au", ".midi", ".mid"],
    "software": [".exe", ".msi", ".jar"],
    "Archives": [".zip", ".rar", ".7z", ".iso", ".cab", ".lzh", ".ace", ".z", ".arc", ".war", ".apk"],
    "src": [".py", ".cpp", ".c", ".java", ".ipynb", ".js", ".ts", ".cs", ".rb", ".go", ".rs", ".swift", ".kt", ".php", ".html", ".css", ".json", ".yaml", ".yml", ".xml", ".sh", ".ps1", ".r", ".lua", ".dart", ".scala", ".pl", ".pm", ".ml", ".hs", ".jl", ".lisp", ".clj", ".ex", ".exs", ".erl", ".hrl", ".pas", ".vhdl", ".verilog", ".asm", ".sql", ".awk", ".tex", ".toml", ".ini", ".cfg", ".makefile", ".dockerfile", ".jenkinsfile", ".gitignore", ".env", ".log"]
}
# reverse it to be able to get the type from the extensions
ext_to_type = {}
for file_type, extensions in file_type_extensions.items():
    for ext in extensions: 
        ext_to_type[ext] = file_type 

# moving the files
for i in source_dir_content: 
        # get full path
        full_path = os.path.join(source_dir, i)
        # skipping the current file (the script)
        if full_path == script_path:
            continue 

        try:
            # checking it's not a dir and itsn't hidden
            if not os.path.isdir(full_path) and not ishidden(full_path):
                # get the file extension
                dot_index = i.rfind('.')
                ext = i[dot_index:]
                # get the fiel category
                file_category_name = ext_to_type.get(ext)
                # checking that the extension has a category
                if file_category_name:
                    destination_dir = paths.get(file_category_name)
                    # checking that the destionan dir exist
                    if destination_dir:
                        try:
                            # move the file
                            shutil.move(full_path, os.path.join(destination_dir, i))
                            print(f"{Colors.GREEN}Moved '{i}' to '{destination_dir}'{Colors.RESET}")
                        except FileNotFoundError:
                            print(f"{Colors.RED}Error: Destination directory '{destination_dir}' not found for '{i}'.{Colors.RESET}")
                        except shutil.Error as e:
                            print(f"{Colors.RED}Error moving '{i}': {e}{Colors.RESET}")
                        except OSError as e:
                            print(f"{Colors.RED}OS Error moving '{i}': {e}{Colors.RESET}")
                    else:
                        print(f"{Colors.YELLOW}Skipping {i}: No destination path defined for category '{file_category_name}'{Colors.RESET}")
                else:  
                    print(f"{Colors.RED}Skipping {i}: Unknown file extension '{ext}'{Colors.RESET}")
        except OSError as e:
                print(f"{Colors.RED}Error checking attributes for {full_path}: {e}")        


# removing the empty folders located in the soruce dir  
for i in source_dir_content: 
        full_path = os.path.join(source_dir, i)
        if os.path.isdir(full_path) and not ishidden(full_path):
            content = os.listdir(full_path)
            if not content: 
                os.rmdir(full_path)
