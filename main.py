import configparser
import pprint
import requests
from bs4 import BeautifulSoup
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
URL = "https://www.billboard.com/charts/hot-100/"

config = configparser.ConfigParser()
print(config.read('env/config.ini'))

SPOTIPY_CLIENT_ID = config['spotify']['client_id']
SPOTIPY_CLIENT_SECRET = config['spotify']['redirect_url']
SPOTIPY_REDIRECT_URI = 'http://example.com'
scope = "playlist-modify-private"

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def has_trucate(class_):
    return class_ and re.compile(r"trucate").search(class_)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

answerDate = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
# answerDate = '2012-02-25'
print(type(answerDate))
print(answerDate)
answerYear = answerDate.split('-')[0]
print(answerYear)

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{answerDate}")
songs_page = response.text
soup = BeautifulSoup(songs_page, "html.parser")
print(soup.title.string)
song = soup.find_all(name="h3", id="title-of-a-story", class_=has_trucate)
print(len(song))
song_list = [s.getText().strip('\n') for s in song]
print(song_list)

#Now lets grab some
song_uri_list = []

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
print(user_id)

for s in song_list:
    tquery = f"track:{s} year:{answerYear}"
    print("Searching...", tquery)

    result = sp.search(tquery, type='track')
    try:
        pprint.pprint(result['tracks']['items'][0]['uri'])
    except IndexError:
        print(f"{s} not found...skipping!")
        continue
    except:
        print("Hit an error...hard stop")
        break
    else:
        print("next...")

    song_uri_list.append(result['tracks']['items'][0]['uri'])

print(song_uri_list)

##Create a playlist
playlist = sp.user_playlist_create(user_id, f"{answerDate} Billboard 100", public=False)
pprint.pprint(playlist)
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uri_list)
