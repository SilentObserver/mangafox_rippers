from mangafox_index_ripper import scrape_manga_index
from ProgressBar import update_progress
import mangafox_ripper as mr
import time

if __name__ == '__main__':
	manga_index_link = input("Enter the link to the manga index:")
	chapter_links = scrape_manga_index(manga_index_link)
	sleep_counter = 0
	completed_count = 0
	update_progress(0)
	for x in chapter_links:
		mr.download_chapter(x)
		sleep_counter +=1
		completed_count += 1
		if sleep_counter == 5:
			time.sleep(5)
			sleep_counter = 0
		update_progress(completed_count/len(chapter_links))
	print("\nDownload Complete")