import argparse
import errno
import hashlib
import logging
import os
import shutil
import signal
import time
import subprocess
import platform


def delete_readonly_file(path):
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
    file_size = os.stat(path).st_size
    if file_size < 1024 * 1024:
        buffer_size = 4096
    elif file_size < 1024 * 1024 * 10:
        buffer_size = 65536
    elif file_size < 1024 * 1024 * 100:
        buffer_size = 1024 * 1024
    else:
        buffer_size = 1024 * 1024 * 10
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def synchronize_folders(source_folder, destination_folder, logger):
    logger.debug(f"Synchronizing folders {source_folder} and {destination_folder}")

    for entry in os.scandir(destination_folder):
        if entry.is_file():
            destination_path = entry.path
            source_path = os.path.join(source_folder, entry.name)
            if not os.path.isfile(source_path):
                logger.info(f"Deleting {destination_path}")
                delete_readonly_file(destination_path)
            else:
                source_hash = get_file_hash(source_path)
                dest_hash = get_file_hash(destination_path)
                if source_hash != dest_hash:
                    try:
                        logger.info(f"Copying {source_path} to {destination_path}")
                        shutil.copy2(source_path, destination_path)
                    except IOError as e:
                        if e.errno == errno.ENOSPC:
                            logger.error("Disk full error occurred. Stopping synchronization.")
                            return
                else:
                    logger.info(f"{destination_path} is up to date")
        elif entry.is_dir():
            subfolder = entry.name
            source_subfolder = os.path.join(source_folder, subfolder)
            destination_subfolder = os.path.join(destination_folder, subfolder)
            if not os.path.isdir(source_subfolder):
                logger.info(f"Deleting {destination_subfolder}")
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
                try:
                    logger.info(f"Copying {source_path} to {destination_path}")
                    shutil.copy2(source_path, destination_path)
                except IOError as e:
                    if e.errno == errno.ENOSPC:
                        logger.error("Disk full error occurred. Stopping synchronization.")
                        return
        elif entry.is_dir():
            subfolder = entry.name
            source_subfolder = os.path.join(source_folder, subfolder)
            destination_subfolder = os.path.join(destination_folder, subfolder)
            if not os.path.isdir(destination_subfolder):
                logger.info(f"Creating directory {destination_subfolder}")
                os.mkdir(destination_subfolder)
            synchronize_folders(source_subfolder, destination_subfolder, logger)


def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("source_folder", help="the path to the source folder")
    parser.add_argument("destination_folder", help="the path to the destination folder")
    parser.add_argument("-i", "--interval", type=int, default=10, help="the synchronization interval in seconds")
    parser.add_argument("-l", "--log-file", help="the path to the log file")

    args = parser.parse_args()

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
