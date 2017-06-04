import requests as rq
from bs4 import BeautifulSoup as bs


def get_manga_indexes(manga_index_page):
	manga_index_soup = bs(rq.get(manga_index_page).content, 'lxml')
	list_of_all_chapter_link_tags = manga_index_soup.find_all("a", {"class": "tips"})
	list_of_all_chapter_links = []
	for link in list_of_all_chapter_link_tags:
		list_of_all_chapter_links.append(link.get('href'))
	list_of_all_chapter_links.sort()
	return list_of_all_chapter_links


def write_manga_indexes_to_file(manga_index_page, index_file_name):
	outFile = open(index_file_name, "w")
	for index_link in get_manga_indexes(manga_index_page):
		outFile.write(index_link)
		outFile.write("\n")
	outFile.close()


if __name__ == '__main__':
	manga_index_page_link = input("Manga index page:")
	output_file_name = input("Output file name:")
	write_manga_indexes_to_file(manga_index_page_link, output_file_name)
