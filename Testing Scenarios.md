1. When both source and destination folders are the same:
In this case, the script should copy all the files and folders from the source folder to the destination folder.

2. When the source folder does not exist:
In this case, the script should exit with an error message indicating that the source folder does not exist.

3. When the destination folder does not exist:
In this case, the script should create the destination folder and copy all the files and folders from the source folder to the destination folder.

4. When a file in the destination folder has been deleted:
In this case, the script should delete the corresponding file from the source folder as well during the synchronization process.

5. When a folder in the destination folder has been deleted:
In this case, the script should delete the corresponding folder from the source folder as well during the synchronization process.

6. When a file in the source folder has been modified:
In this case, the script should copy the modified file from the source folder to the destination folder during the synchronization process.

7. When a new file is added to the source folder:
In this case, the script should copy the new file from the source folder to the destination folder during the synchronization process.

8. When a new folder is added to the source folder:
In this case, the script should create a new folder in the destination folder and copy all the files and folders from the new folder in the source folder to the new folder in the destination folder.
