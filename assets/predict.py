import numpy as np
import string
import re

# pulling respective letter data from 'data' folder 
en = [np.load('data/english_one.npy'), 
	  np.load('data/english_two.npy'), 
	  np.load('data/english_three.npy'),
	  'english']
es = [np.load('data/spanish_one.npy'), 
	  np.load('data/spanish_two.npy'), 
	  np.load('data/spanish_three.npy'),
	  'spanish']
fr = [np.load('data/french_one.npy'), 
	  np.load('data/french_two.npy'), 
	  np.load('data/french_three.npy'),
	  'french']
de = [np.load('data/german_one.npy'), 
	  np.load('data/german_two.npy'), 
	  np.load('data/german_three.npy'),
	  'german']

# converts input to letter characters
def clean(word):
	return re.sub('[^a-zA-Z\n\.]', ' ', word.translate(str.maketrans('','',string.punctuation)))

# converts character to corresponding number
def num(letter):
	letter = letter.lower()
	if letter == ' ': return 0
	return ord(letter) - 96

# converts array of values to percentages of each value
def percents(vals):
	total = sum(vals)
	if total == 0: total = 1 
	percents = [round((var/total)*100, 2) for var in vals]
	return percents

# pulls letter data from previous datasets
def one_chance(letter, lang):
	return lang[0][num(letter)]
def two_chance(letter_a, letter_b, lang):
	return lang[1][num(letter_a)][num(letter_b)]
def three_chance(letter_a, letter_b, letter_c, lang):
	return lang[2][num(letter_a)][num(letter_b)][num(letter_c)]

# calculates the structural similarity of inputted word to each respective language letter structure
def calculate(user_input, lang, a, b, c):
	one_prob = 1
	two_prob = 1
	three_prob = 1
	for letter in user_input:
		one_prob *= one_chance(letter, lang)
	for letter in range(len(user_input)-1):
		two_prob *= two_chance(user_input[letter], user_input[letter+1], lang)
	for letter in range(len(user_input)-2):
		three_prob *= three_chance(user_input[letter], user_input[letter+1], user_input[letter+2], lang)
	return (a*one_prob) + (b*two_prob) + (c*three_prob)

# current user input and processing
user_input = 'I went to the library.'
user_input = clean(user_input.lower())
print('input: ' + user_input + '\n\n' + 'results:' )

results = []
languages = [en, es, fr, de]
for lang in languages:
	# optimal weights: 2, 12, 4
	prob = calculate(user_input, lang, 2, 12, 4)
	results.append((prob, lang[3]))

sort = sorted(results, reverse = True, key=lambda tup: tup[0])
percents = percents([val[0] for val in sort])
for x in range (len(sort)):
	print(sort[x][1] + ": " + str(percents[x]) + '%')