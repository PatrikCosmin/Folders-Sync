**Folder Synchronization Program**

This is a Python program that synchronizes the contents of two folders, keeping them up to date with each other.

**Requirements**

Python 3.6 or later
Usage
To use the program, run it from the command line using the following syntax:

<code> python sync_folders.py source_folder destination_folder [-i INTERVAL] [-l LOG_FILE] </code>

where:

<code> source_folder </code> is the path to the source folder.

<code> destination_folder </code> is the path to the destination folder.

<code> -i INTERVAL </code> (optional) is the synchronization interval in seconds. The default value is 10 seconds.

<code> -l LOG_FILE </code> (optional) is the path to the log file. If not provided, logs will be printed to the console.

**Features**

Folder synchronization between two directories.

Folder content deletion if the source folder content is deleted.

Periodic synchronization according to the specified time interval.

Logging of file creation, copying, removal operations to both console and log file.

Content verification using hash comparison method to ensure file integrity.

**Implementation**

The program works by recursively scanning the source and destination folders for files and subdirectories. If a file exists in the source folder but not in the destination folder, it is copied over. If a file exists in both folders, its contents are compared using SHA-256 hash method to ensure that they are the same. If the contents are different, the file in the destination folder is replaced with the file from the source folder. If a file exists in the destination folder but not in the source folder, it is deleted. If a subdirectory exists in the source folder but not in the destination folder, it is created. If a subdirectory exists in both folders, the same synchronization process is applied recursively to the subdirectories.

**Example:**

To synchronize the contents of C:\FolderA and D:\FolderB with a synchronization interval of 60 seconds and log to a file named sync.log:

<code> python sync_folders.py C:\FolderA D:\FolderB -i 60 -l sync.log </code>
