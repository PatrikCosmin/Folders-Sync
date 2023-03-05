import argparse
import errno
import hashlib
import logging
import os
import shutil
import signal
import time
import platform
import subprocess


def delete_readonly(path):
    if platform.system() == "Windows":
        subprocess.call(["powershell.exe", f"Remove-Item -Path '{path}' -Force"])
    else:
        try:
            os.remove(path)
        except OSError as e:
            if e.errno == errno.EACCES:
                subprocess.call(["sudo", "rm", "-f", path])
            else:
                raise e


def get_file_hash(path):
    hasher = hashlib.md5()
    with open(path, 'rb') as file:
        buffer = file.read(65536)
        while buffer:
            hasher.update(buffer)
            buffer = file.read(65536)
    return hasher.hexdigest()


def synchronize_folders(source_folder, destination_folder, logger):
    logger.debug(f"Synchronizing folders {source_folder} and {destination_folder}")

    for entry in os.scandir(destination_folder):
        if entry.is_file():
            destination_path = entry.path
            source_path = os.path.join(source_folder, entry.name)
            if not os.path.isfile(source_path):
                logger.info(f"{entry.name} is missing in source folder. Deleting {destination_path}")
                delete_readonly(destination_path)
            else:
                source_stat = os.stat(source_path)
                dest_stat = os.stat(destination_path)
                if source_stat.st_mtime > dest_stat.st_mtime:
                    logger.info(f"{entry.name} has been modified. Updating {destination_path}")
                    if platform.system() == "Windows":
                        subprocess.call([
                            "powershell.exe",
                            f"Set-ItemProperty -Path '{destination_path}' -Name IsReadOnly -Value $false"
                        ])
                    shutil.copy2(source_path, destination_path)
                elif source_stat.st_mode != dest_stat.st_mode:
                    logger.info(f"{entry.name} permissions have changed. Updating {destination_path}")
                    if platform.system() == "Windows":
                        subprocess.call([
                            "powershell.exe",
                            f"Set-ItemProperty -Path '{destination_path}' -Name IsReadOnly -Value $false"
                        ])
                    shutil.copy2(source_path, destination_path)
                else:
                    logger.debug(f"{entry.name} is up to date")
        elif entry.is_dir():
            subfolder = entry.name
            source_subfolder = os.path.join(source_folder, subfolder)
            destination_subfolder = os.path.join(destination_folder, subfolder)
            if not os.path.isdir(source_subfolder):
                logger.info(f"{subfolder} is missing in source folder. Deleting {destination_subfolder}")
                shutil.rmtree(destination_subfolder)
            else:
                synchronize_folders(source_subfolder, destination_subfolder, logger)

    for entry in os.scandir(source_folder):
        if entry.is_file():
            source_path = entry.path
            destination_path = os.path.join(destination_folder, entry.name)
            if os.path.isfile(destination_path):
                continue
            else:
                logger.info(f"{entry.name} is new in source folder. Adding {destination_path}")
                shutil.copy2(source_path, destination_path)
        elif entry.is_dir():
            subfolder = entry.name
            source_subfolder = os.path.join(source_folder, subfolder)
            destination_subfolder = os.path.join(destination_folder, subfolder)
            if not os.path.isdir(destination_subfolder):
                logger.info(f"{subfolder} is new in source folder. Creating {destination_subfolder}")
                os.mkdir(destination_subfolder)
            synchronize_folders(source_subfolder, destination_subfolder, logger)


def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("source_folder", help="the path to the source folder")
    parser.add_argument("destination_folder", help="the path to the destination folder")
    parser.add_argument("-i", "--interval", type=int, default=10, help="the synchronization interval in seconds")
    parser.add_argument("-l", "--log-file", help="the path to the log file")

    args = parser.parse_args()

    if not os.path.isdir(args.source_folder):
        print(f"Error: {args.source_folder} is not a valid directory")
        return
    if not os.path.isdir(args.destination_folder):
        print(f"Error: {args.destination_folder} is not a valid directory")
        return

    log_handlers = [logging.FileHandler(args.log_file), logging.StreamHandler()]

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=log_handlers
    )

    logger = logging.getLogger("sync_folders")

    stop_flag = False

    def stop_handler(signum, frame):
        nonlocal stop_flag
        stop_flag = True

    signal.signal(signal.SIGINT, stop_handler)

    while not stop_flag:
        logger.info("Starting folder synchronization")
        synchronize_folders(args.source_folder, args.destination_folder, logger)
        logger.info("Folder synchronization completed")
        time.sleep(args.interval)

    logger.info("Stopping folder synchronization")


if __name__ == "__main__":
    main()
