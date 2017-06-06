import os
import time
from urllib.parse import urljoin

import requests as rq
from bs4 import BeautifulSoup as bs

current_page_url = 0
page_soup = 0


def download_file(file_url, file_path):
    if os.path.exists(file_path):
        print(file_path, "already exists")
        return False
    i = 0
    while i <= 30:
        try:
            file = rq.get(file_url, stream=True)
        except Exception as e:
            print(e)
            print("Sleeping for 5 seconds...")
            time.sleep(5)
            print("Retrying to download file...")

        # noinspection PyUnboundLocalVariable
        if len(file.content) != 0:
            # print("length of file",len(file.content))
            break
        else:
            print("*" * 30)
            print("Error getting", file_path, ": Retry=", i)
            print("*" * 30)
            i += 1

    # file.raw.decode_content = True
    if file.status_code == 200:
        with open(file_path, 'wb') as f:
            # shutil.copyfileobj(file.raw,f)
            f.write(file.content)
            f.flush()
            f.close()
            return True
    return False


def next_page(current_page_soup, current_page_link):  # works
    next_page_link = current_page_soup.find_all('a', {'class': 'next_page'})[0].get('href')
    if ".html" in next_page_link:
        return urljoin(current_page_link, next_page_link)
    else:
        return False


# def get_image_name(image_url): #works
# 	return re.findall('/\S?([0-9_a-z-]+.jpg)\S?',image_url)[0]

def prepare_image_name(image_count):
    return str(image_count) + ".jpg"


def get_image_url(web_page_soup):
    global page_soup
    try:
        image_url = web_page_soup.find('img', {'id': 'image'}).get('src')
    except:
        page_soup = bs(rq.get(current_page_url).content, 'lxml')
        image_url = page_soup.find('img', {'id': 'image'}).get('src')
    return image_url


def get_chapter_name(web_page_soup):
    return web_page_soup.find('h1', {'class': 'no'}).find('a').text


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        return True
    else:
        # print("Error creating", dir_path)
        try:
            print("Removing", dir_path, "directory")
            os.system("rm -rf " + dir_path.replace(' ', '\ '))
            os.mkdir(dir_path)
        except:
            print("Error creating", dir_path)
            return False
        return True


def prepare_file_path(base_path, image_name):
    return base_path + image_name


def download_chapter(start_page, base_path='', return_chapter_name=False):
    global current_page_url
    global page_soup
    current_page_url = start_page
    image_count = 0
    start_page_soup = bs(rq.get(start_page).content, 'lxml')
    if create_dir(base_path + get_chapter_name(start_page_soup)):
        base_path += get_chapter_name(start_page_soup) + "/"
        page_soup = start_page_soup
        page_link = start_page
        while True:
            image_url = get_image_url(page_soup)
            # image_name = get_image_name(image_url)
            image_count += 1
            image_name = prepare_image_name(image_count)
            # print("Downloading", image_name)
            download_file(image_url, prepare_file_path(base_path, image_name))
            next_link = next_page(page_soup, page_link)
            if next_link is False:
                break
            else:
                page_soup = bs(rq.get(next_link).content, 'lxml')
                page_link = next_link
                current_page_url = next_link
        if return_chapter_name:
            return get_chapter_name(start_page_soup)


if __name__ == '__main__':
    chapter_starting_page = input("Manga Chapter Starting page:")
    download_chapter(chapter_starting_page)
    os.system("notify-send \"Rip Complete\" \"Completed ripping chapter from Mangafox.me\"")
# link ="http://h.mfcdn.net/store/manga/13088/03-144.0/compressed/o031.jpg"
# download_file(link,get_image_name(link))
