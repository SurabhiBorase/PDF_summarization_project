import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string

# Ensure required NLTK resources are available
nltk.download('punkt')
nltk.download('stopwords')

def extractive_summarization(text, num_sentences=2):
    if not text.strip():
        return "Error: No text provided for summarization."

    # Tokenize sentences
    sentences = sent_tokenize(text)

    if num_sentences >= len(sentences):
        return "Error: The text is too short for summarization."

    # Tokenize words and remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word.lower() for word in word_tokenize(text) if word.lower() not in stop_words and word not in string.punctuation]

    # Compute word frequency
    word_frequencies = Counter(words)

    # Score sentences based on word frequencies
    sentence_scores = {sentence: sum(word_frequencies[word.lower()] for word in word_tokenize(sentence) if word.lower() in word_frequencies) for sentence in sentences}

    # Select top sentences
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]

    return " ".join(summarized_sentences)

# Get user input
text = input("Enter the text you want to summarize:\n")
try:
    num_sentences = int(input("Enter the number of sentences for the summary:\n"))
except ValueError:
    print("Error: Please enter a valid number.")
    exit()

# Summarize the text
summary = extractive_summarization(text, num_sentences)
print("\nSummary:", summary)
