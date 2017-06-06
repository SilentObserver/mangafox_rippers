import mangafox_full_ripper as mfr

if __name__ == "__main__":
    handler_manga_list = open("manga_list.txt")
    manga_list = handler_manga_list.read().split('\n')

    update_list = []

    for link in manga_list:
        update_list += mfr.auto_update_function(link)

    if len(update_list) is not 0:
        print("New manga chpaters")
        for x in update_list:
            print(x)
# print(manga_list)
