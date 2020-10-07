from nose.tools import assert_equal
from pathlib import Path
from src.functions import process_url
from src.functions import parse_site
from src.functions import create_csv
from src.functions import create_database
import csv
import sqlite3


url1 = 'https://en.wikipedia.org/wiki/London'
url2 = 'http://shakespeare.mit.edu/hamlet/full.html'
url3 = 'shakespeare.mit.edu/hamlet/full.html'
ranked_text = ''


def test_process_url():
    """Test URLs come through in the correct format"""
    processed_url1 = process_url(url1)
    processed_url2 = process_url(url2)
    processed_url3 = process_url(url3)
    assert_equal(processed_url1, url1)
    assert_equal(processed_url2, url2)
    assert_equal(processed_url3, url2)


def test_parse_site():
    """Test that words are listed in descending order"""
    ranked_text = parse_site(url2, 'p')
    for i, word_count_pair in enumerate(ranked_text):
        if i > 1:
            previous_word_count_pair = ranked_text[i-1]
            assert word_count_pair[1] <= previous_word_count_pair[1] 


def test_create_csv():
    """Test csv file exists and that it ranks words in descending order"""
    create_csv(ranked_text)
    csv_file = (Path(__file__).parent / "../data/ranked_text.csv").resolve()
    assert csv_file.exists()
    with open(csv_file) as csvfile:
        r = list(csv.reader(csvfile, delimiter=','))
        for i, count in enumerate(r):
            if i > 1:
                previous_count = r[i-1]
                assert int(count[1]) <= int(previous_count[1]) 


def test_create_database():
    """Test SQL database exists and that it ranks words in descending order"""
    create_database(ranked_text)
    db_file = (Path(__file__).parent / "../data/ranked_text.db").resolve()  
    assert db_file.exists()
    
    connection = sqlite3.connect(db_file)
    c = connection.cursor()

    c.execute("SELECT * FROM ranked_text")
    for i, row in c.fetchall():
        previous_count = c.fetchall()[i-1]
        assert row[1] <= previous_count[1]
    connection.close()
