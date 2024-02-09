import spacy

# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")

######## FUNCTION TO PARSE SENTENCE ##########
#              INPUT : sentence and SpaCy nlp object
#              OUTPUT: sentence score
def parseSentence(sentence, nlp):
    # Process the sentence using SpaCy
    doc = nlp(sentence)

    # DETERMINING IF SENTENCE IS NON GRAMMATICAL OR NOT
    if len(list(doc.sents)) > 0:
        # All linkages found. Grammatically correct
        score = 5
    else:
        # Sentence may be ungrammatical...needs to be checked...
        score = compute_score(doc)

    return score


# Function to compute the score based on linkRatio and nullRatio
def compute_score(doc):
    # Placeholder value for demonstration purposes
    score = 5

    # Extracting relevant information from the SpaCy Doc object
    numOfWords = len(doc)
    numOfLinkages = len(list(doc.sents))
    numOfNullWords = sum([1 for token in doc if token.text.lower() == 'null'])

    # Calculating linkRatio and nullRatio
    linkRatio = float(numOfLinkages) / numOfWords
    nullRatio = float(numOfNullWords) / numOfWords

    # Scoring logic based on linkRatio and nullRatio
    if linkRatio >= 1.0:
        if nullRatio <= 0.1:
            score = 4
        elif 0.1 < nullRatio <= 0.2:
            score = 3
        elif 0.2 < nullRatio <= 0.3:
            score = 2
        elif nullRatio > 0.3:
            score = 1
        else:
            score = 1

    elif 0.5 <= linkRatio <= 1.0:
        if nullRatio < 0.05:
            score = 3
        elif 0.05 < nullRatio <= 0.1:
            score = 2
        elif 0.1 < nullRatio <= 0.15:
            score = 1
        elif nullRatio > 0.15:
            score = 1
        else:
            score = 3

    elif 0.25 <= linkRatio < 0.5:
        if nullRatio < 0.05:
            score = 3
        elif 0.05 < nullRatio <= 0.1:
            score = 2
        elif 0.1 < nullRatio <= 0.15:
            score = 1
        else:
            score = 1

    elif 0.125 <= linkRatio < 0.25:
        if nullRatio < 0.05:
            score = 2
        elif 0.05 < nullRatio <= 0.1:
            score = 1
        else:
            score = 1

    elif linkRatio < 0.125:
        if nullRatio > 0.1:
            score = 1
        else:
            score = 3

    else:
        score = 1

    return score


# Function to check grammar rules and punctuation
def checkGrammarAndPunctuation(sentence):
    # Process the sentence using SpaCy
    doc = nlp(sentence)

    # Placeholder for grammar and punctuation score
    score = 5

    # Check for grammar rules and punctuation
    for token in doc:
        # Example: Check for subject-verb agreement
        if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
            # Incorrect subject-verb agreement detected
            score -= 1

        # Example: Check for adverb placement
        if token.pos_ == "ADV" and token.head.pos_ not in ["VERB", "ADJ"]:
            # Incorrect adverb placement detected
            score -= 1

        # Example: Check for double negation
        if token.text.lower() in ["not", "no", "never"]:
            if token.head.text.lower() in ["not", "no", "never"]:
                # Double negation detected
                score -= 1

        # Example: Check for proper use of conjunctions
        if token.pos_ == "CCONJ" and token.text.lower() not in ["and", "but", "or"]:
            # Incorrect conjunction detected
            score -= 1

        # Example: Check for proper use of commas
        if token.text == "," and token.head.pos_ not in ["PUNCT", "CCONJ"]:
            # Incorrect comma placement detected
            score -= 1

        # Add more grammar and punctuation rules as needed

    return score


##### MAIN FUNCTION TO BE CALLED  ######
#             INPUT : essay
#             OUTPUT: cumulative score(which is the avg sentence score) AND key-value pairs of sentences and its scores
def getGrammarScore(essay):
    # a dictionary to hold sentence and its score
    sentScore = {}

    # Process the entire essay using SpaCy
    doc = nlp(essay)

    for sentence in doc.sents:
        # Combining the scores from grammar check and the original parse function
        sentScore[str(sentence)] = min(parseSentence(str(sentence), nlp), checkGrammarAndPunctuation(str(sentence)))

    # Convert generator to list before using len()
    sentences_list = list(doc.sents)

    # computing cumulative score
    cumScore = float(sum(sentScore.values())) / len(sentences_list)

    return cumScore, sentScore


#### TEST DRIVER FOR TESTING THE MODULE INDEPENDENTLY  ####S
if __name__ == '__main__':
    # Open essay
    sourceFileName = "Sample_Essays/technology.txt"
    sourceFile = open(sourceFileName, "r")

    # Read essay
    essay = sourceFile.read()

    cumscore, sentscore = getGrammarScore(essay)

    for key in sentscore.keys():
        print(key + " :: " + str(sentscore[key]))
        print

    print(cumscore)
