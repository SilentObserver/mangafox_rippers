from bs4 import BeautifulSoup as bs
import requests as rq
from urllib.parse import urljoin
import re
import os


def download_file(file_url,file_path):
	if os.path.exists(file_path):
		print(file_path,"already exists")
		return False
	i=0
	while i<=30:
		file = rq.get(file_url,stream = True)
		if len(file.content) != 0:
			print("length of file",len(file.content))
			break
		else:
			print("*"*30)
			print("Error getting",file_path,": Retry=",i)
			print("*"*30)
			i+=1
	# file.raw.decode_content = True
	if file.status_code == 200:
		with open(file_path,'wb') as f:
			# shutil.copyfileobj(file.raw,f)
			f.write(file.content)
			f.flush()
			f.close()
			return True
	return False

def next_page(web_page_soup,base_url):
	next_page = web_page_soup.find_all('span',{'class':'next'})[0].find('a').get('href')
	if re.match('/\S+/\S+/\S+',next_page) is not None:
		return urljoin(base_url,next_page)
	else:
		return False

def get_image_name(web_page_soup):
	image_no_tag = web_page_soup.find('span',{'class':'c1'})
	image_no = int(re.findall('Page ([0-9]+)',image_no_tag.text)[0])
	image_name = "{0:03d}.jpg".format(image_no)
	return image_name

def get_image_url(web_page_soup):
	return web_page_soup.find_all('img',{'id':'img'})[0].get('src')

def get_chapter_name(web_page_soup):
	return web_page_soup.find('h1').text

def create_dir(dir_path):
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)
		return True
	else:
		print("Error creating",dir_path)
		return False

def prepare_file_path(base_path,image_name):
	return base_path + image_name

def download_chapter(start_page):
	start_page_soup = bs(rq.get(start_page).content,'lxml')
	chpater_name = get_chapter_name(start_page_soup)
	if create_dir(chpater_name):
		base_path = chpater_name+"/"
		base_url = "http://www.mangareader.net/"
		page_soup = start_page_soup
		# page_link = start_page

		while True:
			image_url = get_image_url(page_soup)
			image_name = get_image_name(page_soup)
			print("Downloading", image_name)
			download_file(image_url,prepare_file_path(base_path,image_name))
			next_link = next_page(page_soup,base_url)
			if next_link is False:
				break
			else:
				page_soup = bs(rq.get(next_link).content,'lxml')
				# page_link = next_link

chapter_starting_page = input("Manga Chapter Starting page:")
download_chapter(chapter_starting_page)
# link ="http://h.mfcdn.net/store/manga/13088/03-144.0/compressed/o031.jpg"
# download_file(link,get_image_name(link))
