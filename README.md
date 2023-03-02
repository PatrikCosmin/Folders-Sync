**Folder Synchronization Program**

The Folder Synchronization Program is a Python script that synchronizes two folders, keeping the files in both folders identical. It uses the MD5 hash algorithm to compare the contents of each file and copy only the files that have been modified or added since the last synchronization.

**Installation**

Clone the repository or download the source code.

Install Python 3.x if it is not already installed.

Install the required dependencies by running <code> pip install -r requirements.txt </code>.

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

Folder synchronization between two directories.

Folder content deletion if the source folder content is deleted.

Periodic synchronization according to the specified time interval.

Logging of file creation, copying, removal operations to both console and log file.

Content verification using hash comparison method to ensure file integrity.

FIles are also synchronized when saving with no changes.

**Limitations**

The program is designed to synchronize files, not folders. If you move or rename a folder, it will be treated as a new folder and its contents will be copied to the destination folder.

The program uses the MD5 hash algorithm to compare the contents of each file, which may not be suitable for large files (e.g. > 100 GB) as it requires a lot of memory to calculate the hash. If performance issues may rise with large files, modify the program to use a different hash algorithm or split the file into smaller chunks and hash each chunk separately.

**Implementation**

The program works by recursively scanning the source and destination folders for files and subdirectories. If a file exists in the source folder but not in the destination folder, it is copied over. If a file exists in both folders, its contents are compared using MD5 hash method to ensure that they are the same. If the contents are different, the file in the destination folder is replaced with the file from the source folder. If a file exists in the destination folder but not in the source folder, it is deleted. If a subdirectory exists in the source folder but not in the destination folder, it is created. If a subdirectory exists in both folders, the same synchronization process is applied recursively to the subdirectories.

This program should be able to work with any type of file, as it reads the files in binary mode and synchronizes them based on their binary content using the MD5 hash algorithm. Therefore, the program is file type-agnostic and should work with any file format.

For read-only files and folders **PowerShell** is called using a subprocess for the delete action in Windows based systems.

**Example:**

To synchronize the contents of C:\FolderA and D:\FolderB with a synchronization interval of 60 seconds and log to a file named sync.log:

<code> python sync_folders.py C:\FolderA D:\FolderB -i 60 -l sync.log </code>

Note: Linux type paths are supported since module 'os' is used. Only requirement is to use path separator for Linux, which is a forward slash "/" instead of a backslash "\" used in Windows.
