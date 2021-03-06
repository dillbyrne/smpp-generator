#!/usr/bin/env python
# -*- coding: utf-8  -*-

"""
	Socialist Millionaire Protocol Passphrase Generator
	Version 0.1
    Copyright (C) 2014  dbyrne

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by 
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from random import choice
from itertools import permutations
from math import factorial
import argparse



def build_wordlist(filename):
		
	try:	
		words = [] 
		wordfile = open(filename,'r')


		for line in wordfile:
			for word in line.split():
				if words.count(word) is 0:
					words.append(word) 	
		
		wordfile.close()
		return words

	except IOError,e:
		print "filename {:s} does not exist".format(filename)
		exit()

def generate_phrase(wordlist,numofwords):
	try:	
		phrase = []		

		for i in range(0,numofwords):
			word = choice(wordlist)	
			
			#Ensure one occurrence of each word	
			while phrase.count(word) is not 0:
				word = choice(wordlist)	

			phrase.append(word)
		
		pphrase = ""
		
		for i in range(0,len(phrase)):
			pphrase = pphrase +" "+ phrase[i]		
		
		return pphrase
	except IndexError,e:
		print 'File is empty'
		exit()

def write_phrase_to_file(phrase,filename):
	phrasefile = open(filename,'a')
	phrasefile.write(phrase)
	phrasefile.close()	
	
def	generate_phrase_file(noOfWords,noOfLines,inFile,outFile):
	phraselist =[]	
	wordlist = build_wordlist(inFile)	
	
	numlist = range(0,(len(wordlist)))
	count = 0

	for p in permutations(numlist,noOfWords):
		count+=1
		if count == noOfLines:
			break
	
	if count < noOfLines:
		print "Not enough unique words in input file {:s}".format(inFile)
		exit()
	
	zeros = len(str(noOfLines))


	for i in range(1,noOfLines+1):

		phrase = generate_phrase(wordlist,noOfWords)
		while phraselist.count(phrase) is not 0:
			phrase = generate_phrase(wordlist,noOfWords)
		
		phraselist.append(phrase)
			
		write_phrase_to_file((zeros - len(str(i))) * "0" + str(i)+" "+phrase+"\n",outFile)

	
def main():

	parser = argparse.ArgumentParser(description="Generate a numbered file of"
			" random phrases to be used to verify a person's identity in an OTR"
			" session. You give the person either the list or a line from the" 
			" list in person or by another means such as GPG. Then when the time" 
			" comes to verify during an OTR or similar session, the question can"
			" simply be the number and the answer is the phrase")

	parser.add_argument("noOfWords",type=int,help="The number of words desired in the phrase(s). Max is 20")
	parser.add_argument("noOfLines",type=int,help="The number of phrases to generate. Max is 500")
	parser.add_argument("inFile",type=str,help="The input file used to generate the phrases")
	parser.add_argument("outFile",type=str,help="The output file to save the phrases to")
	
	args = parser.parse_args()
	
	if args.noOfWords > 20:
		print "The number of words per passphrase cannot be more than 20"
		exit()

	if args.noOfLines > 500:
		print "The number of passphrases cannot be more than 500"
		exit()

	generate_phrase_file(args.noOfWords,args.noOfLines,args.inFile,args.outFile)

if __name__ == "__main__":
	main()
