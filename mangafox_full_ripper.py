import os
import time

import mangafox_index_ripper as index_ripper
import mangafox_ripper as chapter_ripper
from ProgressBar import update_progress

FILE_NAME = "completed_links.inli"


def check_or_create_links_list(link, path=''):
    if not os.path.exists(path + FILE_NAME):
        new_links_file = open(path + FILE_NAME, "w")
        new_links_file.write(link + '\n')
        new_links_file.close()


def download_complete_manga(manga_index_link, base_path='', return_update_list=False):
    chapter_links = index_ripper.get_manga_indexes(manga_index_link)

    check_or_create_links_list(manga_index_link, base_path)

    completed_links_file = open(base_path + FILE_NAME, "r")
    completed_links = completed_links_file.read().split("\n")
    completed_links_file.close()
    completed_links_file = open(base_path + FILE_NAME, "a")
    sleep_counter = 0
    completed_count = 0
    update_progress(0)
    update_list = []
    try:
        for x in chapter_links:
            if x not in completed_links:
                if return_update_list:
                    chapter_name = chapter_ripper.download_chapter(x, base_path, return_chapter_name=True)
                    update_list.append(chapter_name)
                else:
                    chapter_ripper.download_chapter(x, base_path)

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
        if not return_update_list:
            return True
        else:
            return update_list
    except:
        print("Error occurred while downloading. Retrying...")
        if return_update_list:
            update_list += download_complete_manga(manga_index_link, base_path, return_update_list)
            return update_list
        else:
            download_complete_manga(manga_index_link, base_path, False)
            return True


def create_or_check_for_base_folder(link):
    manga_title = link.split('/')[-2].replace('_', ' ').title()
    if not os.path.exists(manga_title):
        os.mkdir(manga_title)
    path = manga_title + '/'
    return path


def auto_update_function(link):
    path = create_or_check_for_base_folder(link)
    return download_complete_manga(link, path, True)


if __name__ == '__main__':
    print("Version1.2")
    index_link = input("Enter the link to the manga index:")
    new_base_path = create_or_check_for_base_folder(index_link)
    status = download_complete_manga(index_link, new_base_path)
    if status:
        print("\nDownload Complete")
        # Desktop Notification in Ubuntu
        os.system("notify-send \"Download Complete\" \"Completed Downloading manga\"")
    else:
        print("\nDownload Failed")
        # Desktop Notification in Ubuntu
        os.system("notify-send \"Download Failed\" \"Failed to Download manga\"")
