**Folder Synchronization Program**

This program synchronizes two folders by copying files from the source folder to the destination folder if they are new or have been modified since the last synchronization. It also deletes files from the destination folder if they do not exist in the source folder.

**Installation**

Clone the repository or download the source code.

Install Python 3.x if it is not already installed.

**Instructions**

To use the program, run it from the command line using the following syntax:

<code> python sync_folders.py source_folder destination_folder [-i INTERVAL] [-l LOG_FILE] </code>

where:

<code> source_folder </code> is the path to the source folder.

<code> destination_folder </code> is the path to the destination folder.

<code> -i INTERVAL </code> (optional) is the synchronization interval in seconds. The default value is 10 seconds.

<code> -l LOG_FILE </code> (optional) is the path to the log file. If not provided, logs will be printed to the console.

To stop the program, press <code> Ctrl + C </code> while in terminal.

**Features**

Synchronizing two folders by copying new or modified files from the source folder to the destination folder, and deleting files from the destination folder that do not exist in the source folder.

Logging information about the synchronization process to both the console and an optional log file.

Specifying the synchronization interval in seconds as a command-line argument (default is 10 seconds).

Handling interruptions by the user (e.g., by pressing Ctrl+C) and logging a message indicating that synchronization has stopped.

Using the md5 hash of each file to determine whether it has been modified since the last synchronization.

Handling different file permissions and ownership on different platforms (Windows and Linux).

Checking if the source and destination folders exist and are valid directories before synchronizing.

Providing helpful error messages if the source or destination folders are not valid directories.

**Limitations**

The program uses the md5 hash of each file to determine whether it has been modified since the last synchronization. This means that if the contents of a file are changed without changing its size or modification time, the program will not detect the change and will not copy the new contents to the destination folder. This can lead to data loss or inconsistency if the modified file is critical.

The program does not handle conflicts that may arise when a file is modified in both the source and destination folders between synchronizations. In such cases, it may overwrite one of the modified files with the other, depending on the modification times.

The program assumes that the source and destination folders have the same structure and naming conventions. If the folders have different structures or naming conventions, the program may fail to synchronize some files or subfolders.

The program does not handle errors that may occur during file copying or deletion. For example, if a file is locked by another process or the user does not have sufficient permissions to copy or delete a file, the program will raise an exception and terminate.

The program does not provide any progress indication during synchronization, which can be useful for large folders or slow network connections.

The program does not handle files with Unicode characters or file paths longer than the maximum allowed by the operating system. This can lead to errors or unexpected behavior when copying or deleting such files.

The program only supports Windows and Linux platforms. It may not work correctly or at all on other platforms.

**Implementation**

The program imports several Python modules, including argparse, errno, hashlib, logging, os, shutil, signal, time, platform, and subprocess.

The program defines a function called delete_readonly that takes a file path as an argument. If the operating system is Windows, the function calls subprocess.call to run a PowerShell command that deletes the file even if it is read-only. Otherwise, the function tries to delete the file using os.remove. If os.remove raises an OSError with an error number of errno.EACCES (which indicates a permissions error), the function calls subprocess.call to run a sudo rm command that deletes the file as the superuser.

The program defines a function called get_file_hash that takes a file path as an argument. The function uses the hashlib module to calculate the md5 hash of the file's contents and returns the hash as a hexadecimal string.

The program defines a function called synchronize_folders that takes the paths of a source folder, a destination folder, and a logger object as arguments. The function first logs a message indicating that it is synchronizing the folders.

The function then uses a for loop to iterate over each entry in the destination folder using os.scandir. For each file in the destination folder, the function checks if the corresponding file exists in the source folder. If the file does not exist in the source folder, the function logs a message indicating that the file is missing in the source folder and calls delete_readonly to delete the file from the destination folder. If the file exists in the source folder, the function compares the modification times and permissions of the source and destination files. If the source file has been modified more recently or has different permissions, the function logs a message indicating that the file has been modified or that its permissions have changed and copies the file from the source folder to the destination folder using shutil.copy2. If the file is up to date, the function logs a message indicating that the file is up to date.

The function then uses another for loop to iterate over each entry in the source folder using os.scandir. For each file in the source folder, the function checks if the corresponding file exists in the destination folder. If the file does not exist in the destination folder, the function logs a message indicating that the file is new in the source folder and copies the file from the source folder to the destination folder using shutil.copy2.

The function also handles subfolders recursively by using nested for loops to synchronize each subfolder in the source and destination folders.

The main function uses argparse to parse command-line arguments, checks if the source and destination folders are valid directories, sets up logging to both the console and an optional log file, registers a signal handler to handle interruptions by the user, and runs a loop that repeatedly synchronizes the folders with a specified interval between synchronizations.

Finally, the program checks if the __name__ variable is set to '__main__' (indicating that the program is being run as a script rather than imported as a module) and calls the main function if it is.

This program should be able to work with any type of file, as it reads the files in binary mode and synchronizes them based on their binary content using the MD5 hash algorithm. Therefore, the program is file type-agnostic and should work with any file format.

For read-only files and folders **PowerShell** is called using a subprocess for the delete action in Windows based systems.

**Example:**

To synchronize the contents of C:\FolderA and D:\FolderB with a synchronization interval of 60 seconds and log to a file named sync.log:

<code> python sync_folders.py C:\FolderA D:\FolderB -i 60 -l sync.log </code>

Note: Linux type paths are supported since module 'os' is used. Only requirement is to use path separator for Linux, which is a forward slash instead of a backslash used in Windows.
