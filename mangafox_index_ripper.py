import urllib as ul
from bs4 import BeautifulSoup as bs
import requests as rq

def scrape_manga_index(manga_index_page):
	manga_index_soup = bs(rq.get(manga_index_page).content,'lxml')
	list_of_all_chapter_link_tags = manga_index_soup.find_all("a",{"class":"tips"})
	list_of_all_chapter_links = []
	for link in list_of_all_chapter_link_tags:
		list_of_all_chapter_links.append(link.get('href'))
	list_of_all_chapter_links.sort()
	return list_of_all_chapter_links
if __name__ == '__main__':
	manga_index_page_link = input("Manga index page:")
	chapter_links = scrape_manga_index(manga_index_page_link)
	for x in chapter_links:
		print(x)
	print("No. of Chapters:",len(chapter_links))
