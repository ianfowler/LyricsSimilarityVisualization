# Ian Fowler, Digital Literary Studies, 2019
from PyLyrics import *
import csv

# Reads the text file in the folder filled with the same stop words that voyant uses
voyantStopWords = open("voyantStopWords.txt", "r").read().split("\n") # From this site: https://voyant-tools.org/

# Adds a given artist name, album name, and album lyrics to the local database.
def add_row_to_csv(artist, album, lyrics): # Must have a .csv file in the current directory named 'db.csv'
	# using https://stackoverflow.com/a/37654233
	fields=[artist, album, lyrics]
	with open(r'db.csv', 'a') as f:
		writer = csv.writer(f)
		writer.writerow(fields)

# Removes stop words and new lines from a song's lyrics. Filters out any html code that may have accidentally made it in the song lyrics.
def filter_lyrics(lyrics):
	flat = lyrics.replace("\n"," ").replace("\r"," ")
	while "  " in flat:
		flat = flat.replace("  "," ")

	word_arr = flat.split()
	filtered_word_arr  = [word for word in word_arr if (word.lower() not in voyantStopWords) and not ("<" in word or "/" in word or "=" in word or ":" in word or "\"" in word)] # with a little help from: https://stackoverflow.com/a/25346119
	filtered_lyrics = ' '.join(filtered_word_arr)
	return filtered_lyrics

# Prompts the user to add a given artist's albums, one-by-one. It is up to the user to filter live and studio albums manually.
def add_artist(name):
	albums = PyLyrics.getAlbums(singer=name)
	for album in albums:
		print("Include " + album.name + "?")
		response = input("y/n: ")
		if response.lower().strip() == "y":
			lyrics_collection = ""
			for track in album.tracks():
				try:
					lyrics_collection += filter_lyrics(track.getLyrics())
				except ValueError:
					print("Couldn't get lyrics for " + track.name + ". Moving on!")
			
			add_row_to_csv(name, album.name, lyrics_collection)

# Repeatedly prompts the user to add artists.
while True:
	artist = input("What artist would you like to add to the database? ")
	add_artist(artist)

