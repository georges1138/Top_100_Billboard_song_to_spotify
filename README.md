# Top_100_Billboard_song_to_spotify
Python app that creates spotify songlist by webscraping Billboard webpages.  Uses modules: requests, BeautifulSoup and spotipy

Python script takes a specific year from the user input and will open the Top 100 songs for that year from the Billboard charts webpage.  Then will "scrape" the list of 
songs from that year and contact the Spotify songlist server via the spotify object including OAuth for authentication.

For each song on the list, will search on Spotify via the given year and add it to a custom song playlist.
