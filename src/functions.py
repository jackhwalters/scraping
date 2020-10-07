from collections import Counter
from string import punctuation
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import csv
import sqlite3

base_path = Path(__file__).parent


def process_url(url):
    """Correctly format user inputted URL"""
    print("\nProcessing URL...")
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    else:
        url = f'{url}'
    print('Done.\n')
    return url


def parse_site(url, HTML_pref):
    """Retrieve site HTML, rank text of user-defined HTML preference and
    rank in list starting from the most common"""
    print("Parsing site HTML...")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    text = (''.join(s.findAll(text=True))for s in soup.findAll(f'{HTML_pref}'))
    c = Counter((x.rstrip(punctuation).lower() for y in text for x in y.split()))
    ranked_text = c.most_common()
    print('Done.\n')
    return ranked_text


def create_csv(ranked_text):
    """Write word and count pairs into individual rows of a csv file"""
    print("Creating CSV...")
    csv_file = (base_path / "../data/ranked_text.csv").resolve()
    try:
        with open(csv_file, 'w') as csvfile:
            w = csv.writer(csvfile, delimiter=',')
            w.writerow(['Word', 'Count'])
            for i in ranked_text:
                w.writerow(i)
    except IOError:
        print("Input/Output error")


def create_database(ranked_text):
    """Write word and count pairs into individual rows of an SQL database"""
    db_path = (base_path / "../data/ranked_text.db").resolve()
    if not db_path.exists():
        print("Creating database...")
        db_file = Path(db_path)
        connection = sqlite3.connect(db_file)
        c = connection.cursor()
        c.execute('''CREATE TABLE ranked_text (
                Word text,
                Count integer
                )''')
    elif db_path.exists():
        print("Updating database...")
        db_file = Path(db_path)
        connection = sqlite3.connect(db_file)
        c = connection.cursor()

    c.executemany('INSERT INTO ranked_text VALUES (?, ?)', ranked_text)
    connection.close()


def process(url_raw, text_pref):
    """Container URL processing, site parsing, and csv file/database
    creation"""
    HTML_dict = {'all': 'p', 'bold': 'b', 'italic': 'i'}
    try:
        processed_url = process_url(url_raw)
    except IndexError:
        print("ERROR: No URL argument found.")

    try:
        ranked_text = parse_site(processed_url, HTML_dict[text_pref])
    except KeyError:
        print("ERROR: Word type selection unrecognised")

    try:
        create_csv(ranked_text)
        print('Done.\n')
    except KeyError or UnboundLocalError:
        print("ERROR: Selection not recognised, failed to create CSV file.")

    try:
        create_database(ranked_text)
        print('Done.\n')
    except sqlite3.OperationalError:
        print("ERROR: Failed to create database")
    except AttributeError:
        print("ERROR: Failed to create database")
