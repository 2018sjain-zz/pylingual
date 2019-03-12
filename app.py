from flask import Flask, request, render_template
app = Flask(__name__)

# Language by Letters Assessment
# Based on "Machine Learning Assessment for Language Identification Based on Letter and Next Letter Frequency"
# Visit at: http://sachinjain.org/assets/SachinJainSiemensResearchPaper.pdf

import numpy as np
import string
import re

en = [np.load('assets/data/english_one.npy'), 
	  np.load('assets/data/english_two.npy'), 
	  np.load('assets/data/english_three.npy'),
	  'english']
es = [np.load('assets/data/spanish_one.npy'), 
	  np.load('assets/data/spanish_two.npy'), 
	  np.load('assets/data/spanish_three.npy'),
	  'spanish']
fr = [np.load('assets/data/french_one.npy'), 
	  np.load('assets/data/french_two.npy'), 
	  np.load('assets/data/french_three.npy'),
	  'french']
de = [np.load('assets/data/german_one.npy'), 
	  np.load('assets/data/german_two.npy'), 
	  np.load('assets/data/german_three.npy'),
	  'german']

# converts input to letter characters
def clean(word):
	return re.sub('[^a-zA-Z\n\.]', ' ', word.translate(str.maketrans('','',string.punctuation)))

# converts character to corresponding number
def char2num(letter):
	letter = letter.lower()
	if letter == ' ': return 0
	return ord(letter) - 96

# converts array of values to percentages of each value
def arr2pct(values):
	total = sum(values)
	if total == 0: total = 1 
	percents = [round((value/total)*100, 2) for value in values]
	return percents

# pulls letter data from previous datasets
def singlePct(a, lang):
	return lang[0][char2num(a)]
def doublePct(a, b, lang):
	return lang[1][char2num(a)][char2num(b)]
def triplePct(a, b, c, lang):
	return lang[2][char2num(a)][char2num(b)][char2num(c)]

# calculates the structural similarity of inputted word to each respective language letter structure
def probability(user_input, lang, wa, wb, wc):
	singleProb = 1
	doubleProb = 1
	tripleProb = 1
	for letter in user_input:
		singleProb *= singlePct(letter, lang)
	for letter in range(len(user_input)-1):
		doubleProb *= doublePct(user_input[letter], user_input[letter+1], lang)
	for letter in range(len(user_input)-2):
		tripleProb *= triplePct(user_input[letter], user_input[letter+1], user_input[letter+2], lang)
	return (wa*singleProb) + (wb*doubleProb) + (wc*tripleProb)

def calculate(user_input):
	user_input = clean(user_input.lower())
	results = []
	languages = [en, es, fr, de]
	for lang in languages:
		# optimal weights: 2, 12, 4
		output = probability(user_input, lang, 2, 12, 4)
		results.append((output, lang[3]))
	sort = sorted(results, reverse = True, key=lambda tup: tup[0])
	percents = arr2pct([val[0] for val in sort])
	output = {}
	output['input'] = user_input
	output['data'] = {}
	for x in range(len(sort)):
		output['data'][sort[x][1]] = str(percents[x]) + "%"
	return output

# End of Language by Letters Assessment
# Contact sj6hk@virginia.edu for Questions

# @app.route('/test')
# def test():
# 	example = calculate("increasing")
# 	data = example['data']
# 	language = next(iter(data))
# 	return language + ": " + data[language]

@app.route('/')
def index():
	return render_template('main.html')

@app.route('/', methods = ['POST'])
def calculateResults():
	user_input = request.form["input"]
	if clean(user_input) == "":
		return render_template('main.html')
	output = calculate(user_input)
	return render_template("results.html", data = output)

if __name__ == '__main__':
    app.run()