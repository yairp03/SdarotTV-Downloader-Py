from series import Series

def main():
    print("Hi! Welcome to the Sdarot TV downloader.")
    first_episode_url = get_first_episode_url()
    series = Series(first_episode_url)
    series.print_data() # TO REMOVE
    

def get_first_episode_url():
    return input("Enter first episode url (something like https://sdarot.space/watch/$series$/season/1/episode/1):\n")


if __name__ == "__main__":
    main()
