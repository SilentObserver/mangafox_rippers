import os
import time

import mangafox_index_ripper as index_ripper
import mangafox_ripper as chapter_ripper
from ProgressBar import update_progress


def download_complete_manga(manga_index_link):
    chapter_links = index_ripper.get_manga_indexes(manga_index_link)
    completed_links_file = open("completed_links.inli", "r")
    completed_links = completed_links_file.read().split("\n")
    completed_links_file.close()
    completed_links_file = open("completed_links.inli", "a")
    sleep_counter = 0
    completed_count = 0
    update_progress(0)
    try:
        for x in chapter_links:
            if x not in completed_links:
                chapter_ripper.download_chapter(x)
                sleep_counter += 1
                completed_links.append(x)
                completed_links_file.write(x)
                completed_links_file.write("\n")
                completed_links_file.flush()
            completed_count += 1

            if sleep_counter == 5:
                time.sleep(5)
                sleep_counter = 0
            update_progress(completed_count / len(chapter_links))
        return True
    except:
        print("Error occurred while downloading")


if __name__ == '__main__':
    print("Version1.2")
    index_link = input("Enter the link to the manga index:")
    status = download_complete_manga(index_link)
    if status:
        print("\nDownload Complete")
        # Desktop Notification in Ubuntu
        os.system("notify-send \"Download Complete\" \"Completed Downloading manga\"")
    else:
        print("\nDownload Failed")
        # Desktop Notification in Ubuntu
        os.system("notify-send \"Download Failed\" \"Failed to Download manga\"")
