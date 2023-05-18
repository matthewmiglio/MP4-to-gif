import os


# method to count the number of files in a folder
def count_files_in_folder(folder_path):
    file_count = 0
    for _, _, files in os.walk(folder_path):
        file_count += len(files)
    return file_count


# method to get the appdata folder path
def get_appdata_folder():
    appdata_path = os.getenv("APPDATA")
    return appdata_path


# method to make a folder to a given path
def create_folder(folder_path):
    try:
        os.mkdir(folder_path)
        print("Folder created successfully at:", folder_path)
    except OSError:
        print("Error creating folder at:", folder_path)


# method to check if a file exists
def folder_exists(folder_path):
    return os.path.exists(folder_path)

def get_next_mp4_save_path():
    path = get_appdata_folder() + r'\\Py-VideoConverter\\mp4_videos'
    path += f'\\video{count_files_in_folder(path)+1}.mp4'
    return path

    
def get_next_gif_save_path():
    path = get_appdata_folder() + r'\\Py-VideoConverter\\gif_videos'
    path += f'\\video{count_files_in_folder(path)+1}.gif'
    return path

# method to save a file to a given location
def save_file(file_content):
    file_path = get_appdata_folder() + "\\Py-VideoConverter"
    file_name = f"Video{count_files_in_folder()+1}"

    try:
        with open(file_path + "\\" + file_name, "w") as file:
            file.write(file_content)
            file.close()
    except OSError:
        print("Error saving file at:", file_path + "\\" + file_name)


main_dir = get_appdata_folder() + "\\Py-VideoConverter"
if not folder_exists(main_dir):
    create_folder(main_dir)

mp4_vids_dir = main_dir + "\\mp4_videos"
if not folder_exists(mp4_vids_dir):
    create_folder(mp4_vids_dir)

gif_vids_dir = main_dir + "\\gif_videos"
if not folder_exists(gif_vids_dir):
    create_folder(gif_vids_dir)
