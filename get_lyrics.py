import sys, requests
from bs4 import BeautifulSoup
import re
import os
import nltk
from matplotlib import pyplot as plt
from afinn import Afinn

defaults = {
    'request': {
        'token': 'FpOXt73TnxHjdHDeF0kwIFDipNgN7qApJrHg1smrdQSFSrUEsjzWhuoQ7mKglhPi',
        'base_url': 'https://api.genius.com'
    },
    'message': {
        'search_fail': 'The lyrics for this song were not found!',
        'wrong_input': 'Wrong number of arguments.\n' \
                       'Use two parameters to perform a custom search ' \
                       'or none to get the song currently playing on Spotify.'
    }
}

def request_song_info(song_title, artist_name):
    base_url = defaults['request']['base_url']
    headers = {'Authorization': 'Bearer ' + "FpOXt73TnxHjdHDeF0kwIFDipNgN7qApJrHg1smrdQSFSrUEsjzWhuoQ7mKglhPi"}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response

def scrap_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics

def main(song_title, artist_name):
    response = request_song_info(song_title, artist_name)
    json = response.json()
    remote_song_info = None

    for hit in json['response']['hits']:
        if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
            break

    # Extract lyrics from URL if song was found
    if remote_song_info:
        song_url = remote_song_info['result']['url']
        lyrics = scrap_song_url(song_url)
        return lyrics
    else:
        print song_title
        print(defaults['message']['search_fail'])
        return None

# Get a list of stopwords from nltk
stopwords = nltk.corpus.stopwords.words("english")

def get_clean_words(wordsss):
    def _isnum(w):
        try:
            int(w)
            return True
        except ValueError:
            return False

    # Remove table and external links
    markup_text = re.sub(r'\{\{[\s\S]*?\}\}', '', wordsss)

    # Remove category links
    markup_text = re.sub(r'\[\[Category.+\]\]', '', markup_text)

    # Set words to lowercase and remove them if they are stop words
    words = [w.lower() for w in re.findall('\w+', markup_text) if w.lower() not in stopwords]

    # Remove numbers
    words = [w for w in words if not _isnum(w)]

    word_string = ""
    for word in words:
        word_string += word + " "

    return word_string

def get_sentiment_score(words):
    if words:
        text = get_clean_words(words)        #set text to the string produced by get_clean_words
        word_list = text.split()                         #split the string into a list of words
        num_words = len(word_list)                       #get the number of words in the list
        afinn = Afinn()                                  #initiate Afinn
        score = afinn.score(text)                        #find the Afinn score for the text string
        avg = score/num_words                            #find the average Afinn score per word
        return avg
    else:
        return None


def sentiment(title, artist):
    lyrics = main(title, artist)
    score = get_sentiment_score(lyrics)
    return score
