import json
from collections import Counter
from itertools import groupby, product


# newline-delimited list of UA destination cities from Wikipedia
data_file_in = 'cities.txt'

# JSON file to write data into
data_file_out = 'cheers.json'

# the word we're trying to make
phrase = 'CHEERS'

# count up the letter occurances for later comparison
phrase_counter = Counter(phrase)

# make a dict out of the phrase with letters as keys and index
# position as value -- will use this later for a custom alpha sort
phrase_dict = {val: idx for idx, val in enumerate(phrase)}

# main dict to hold the data for the first pass through
data = {}

# open the cities file and read the data into a list
with open(data_file_in, 'r') as infile:
    cities = infile.read().splitlines()

# loop over the list of cities
for city in cities:

    # loop over the letters in the city name, and
    # grab the index number along with the letter
    for i, letter in enumerate(city):

        # if the letter is in the phrase of interest
        if letter in phrase:

            # check to see if this top-level index position key already exists
            if data.get(i):
                # add onto an existing string keeping track of all
                # the useable letters
                data[i]['string'] += letter

                # and drop the city name into a separate list
                data[i]['letter_data'].append(city)
            else:
                # or start a new record, same jam
                data[i] = {
                    'string': letter,
                    'letter_data': [city]
                }

# the main dict that will be exported to file --
# keeping track not just of the data to render on the page
# but also a counter for how many unique combinations exist
data_final = {
    'data': {},
    'possible_combinations': 0
}

# loop over that object we just made
for idx in data:

    # get a handle to the data for this letter position
    record = data[idx]

    # grab the giant string of letters from the city names
    string = record['string']

    # and the actual city list
    letter_data = record['letter_data']

    # count up the occurrences of each letter in that big string
    string_counter = Counter(string)

    # see what you're left with when you subtract this from
    # the phrase counter set up earlier
    diff = phrase_counter - string_counter

    # if there's no difference -- in other words, if there
    # will be enough city names to spell out the phrase --
    # then include it, otherwise ignore it
    if not diff:

        # sort the list of cities by the letter in the index
        # position we're currently operating on, and
        # default to a big number if the letter isn't in the dict
        ld_sorted = sorted(
            letter_data,
            key=lambda word: phrase_dict.get(word[idx], 999)
        )

        # now group that list by the letter position of interest
        ld_grouped = groupby(ld_sorted, key=lambda x: x[idx])

        # and arrange it as a key/value pair, with the letter
        # as a key and the list as a value
        ld_arranged = {k: list(g) for k, g in ld_grouped}

        # get the length of the cartesian product representing
        # all possible combinations of combining these lists
        no_combos = len(list(product(*[ld_arranged[x] for x in ld_arranged])))

        # add the number of combinations to the running total
        data_final['possible_combinations'] += no_combos

        # add the list of as the value mapped to letter index
        data_final['data'][idx] = ld_arranged


# format the total number of combinations with a comma
data_final['possible_combinations'] = '{:,}'.format(data_final['possible_combinations'])  # noqa

# dump the data to file
with open(data_file_out, 'w') as outfile:
    json.dump(data_final, outfile)
