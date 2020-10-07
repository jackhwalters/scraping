from functions import process


# Prompt user input for URL and HTML type to parse, then call process()
# function
print('''\nPlease enter the URL of the site you'd like to process\n''')
url_raw = input('> ')
print('''\nPlease select type of words to rank:
    all, bold or italic text\n''')
text_pref = input('> ')
process(url_raw, text_pref)
