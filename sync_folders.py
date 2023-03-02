import argparse
import hashlib
import logging
import os
import shutil
import signal
import time

def get_file_hash(path):
    with open(path, "rb") as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()


def synchronize_folders(source_folder, destination_folder, logger):
    logger.debug(f"Synchronizing folders {source_folder} and {destination_folder}")


    if not os.path.isdir(source_folder):
        logger.error(f"Source folder {source_folder} does not exist")
        return
    if not os.path.isdir(destination_folder):
        logger.error(f"Destination folder {destination_folder} does not exist")
        return

    for entry in os.scandir(destination_folder):
        if entry.is_file():
            destination_path = entry.path
            source_path = os.path.join(source_folder, entry.name)
            if not os.path.isfile(source_path):
                logger.info(f"Deleting {destination_path}")
                os.remove(destination_path)
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
                source_mtime = os.path.getmtime(source_path)
                dest_mtime = os.path.getmtime(destination_path)
                if source_mtime > dest_mtime:
                    logger.info(f"Copying {source_path} to {destination_path}")
                    shutil.copy2(source_path, destination_path)
                else:
                    logger.info(f"{destination_path} is up to date")
            else:
                logger.info(f"Copying {source_path} to {destination_path}")
                shutil.copy2(source_path, destination_path)
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

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", handlers=[logging.FileHandler(args.log_file), logging.StreamHandler()])

    logger = logging.getLogger("sync_folders")

    stop_flag = False

    def stop_handler(signal, frame):
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
