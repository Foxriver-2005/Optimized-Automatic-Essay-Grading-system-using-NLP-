import enchant
import re

########## function which checks spellings ##############
# 		INPUT : essay
# 		OUTPUT: returns the number of misspelt words AND key-value pairs of missplet words and suggestions to correct them

def spellCheck(text):
	#choose the dictionary
	d = enchant.Dict("en_US")
	
	#keep track of the number of misspelt words
	numIncorrect=0
	
	#split the text into words
	wordList = re.findall(r'\w+', text)
	
	misspelt = {}
	
	### Checking for misspelt words ###
	for word in wordList:
		#print word, d.check(word)
		if d.check(word)==False:
			misspelt[word] = d.suggest(word)	#store the word and its suggestions as a key value pair
			numIncorrect += 1
			
	return numIncorrect, misspelt




######  INDEPENDENTLY TESTING THE SCRIPT ########
if __name__ == '__main__' :
	
	#### open essay, in the format (.txt) ####
	sourceFileName = "Sample_Essays/technology.txt"
	sourceFile = open(sourceFileName, "r")
	
	#read essay
	text = sourceFile.read()
	
	incorr2, misspelt2 = spellCheck(text)
	print ("\n\nIncorrectly spelled count: ", incorr2, "\n")
	
	for key in misspelt2:
		print (key, " :: ",  misspelt2[key], "\n\n")
	
	
