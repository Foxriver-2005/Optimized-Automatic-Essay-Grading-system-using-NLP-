from sentence_transformers import SentenceTransformer
from bert_score import score
import spacy

# Load pre-trained BERT model for sentence embeddings
sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")

def check_coherence(essay):
    # Extract sentences from the essay
    sentences = [sent.text for sent in nlp(essay).sents]

    # Check logic and consistency based on logical connectors
    logic_consistency_score = calculate_logic_consistency(sentences)

    # Calculate semantic similarity using BERT
    semantic_similarity_score = calculate_semantic_similarity(essay, sentences)

    # Normalize logic and consistency score based on the number of sentences
    max_score = 5  # Maximum score for coherence
    logic_consistency_score = min(logic_consistency_score, max_score)
    logic_consistency_score /= max_score

    # Combine the scores based on your requirements
    coherence_score = (logic_consistency_score + semantic_similarity_score) / 2 * 5

    return coherence_score

def calculate_logic_consistency(sentences):
    # Initialize logic and consistency score
    logic_consistency_score = 0

    # Example: Check for logical connectors (e.g., "but", "however") in the essay
    for sentence in sentences:
        if has_logical_connectors(sentence):
            logic_consistency_score += 1
            print(f"Logical connection in the sentence: {sentence}")
            print(f"Logical connection score: {logic_consistency_score}")
            print()

    return logic_consistency_score

def has_logical_connectors(sentence):
    # Example: Check for logical connectors in a sentence
    logical_connectors = ["but", "however", "although", "yet", "while", "even though", "on the other hand", "in contrast", "nevertheless", "nonetheless", "conversely", "still", "despite", "in spite of"]  # Customize based on your needs
    tokenized_sentence = nlp(sentence.lower())
    
    for token in tokenized_sentence:
        if token.text in logical_connectors:
            return True

    return False

def calculate_semantic_similarity(essay, sentences):
    # Calculate semantic similarity using BERT
    reference_sentences = ["This is a reference sentence."] * len(sentences)  # You can customize this based on your needs
    candidate_sentences = list(sentences)

    _, _, semantic_similarity_score = score(candidate_sentences, reference_sentences, lang='en', model_type='bert-base-uncased', verbose=True)
    print("Semantic score")
    print(semantic_similarity_score)

    return semantic_similarity_score.mean().item()

def get_logical_sentences(essay):
    sentences = [sent.text for sent in nlp(essay).sents]
    logical_sentences = []

    for sentence in sentences:
        if has_logical_connectors(sentence):
            logic_consistency_score = 1  # You can modify this based on your needs
            logical_sentences.append({'sentence': sentence, 'score': logic_consistency_score})

    return logical_sentences


if __name__ == "__main__":
    # Example usage
    sourceFileName = "Sample_Essays/technology.txt"
    sourceFile = open(sourceFileName, "r")
    essay = sourceFile.read()

    coherence_score = check_coherence(essay)
    logical_sentences = get_logical_sentences(essay)

    # Display the coherence score
    print(f"Coherence Score: {coherence_score}")

    # Display the logical sentences and their scores
    for logical_sentence in logical_sentences:
        print(f"Logical Sentence: {logical_sentence['sentence']}")
        print(f"Logical Sentence Score: {logical_sentence['score']}")
        print()
