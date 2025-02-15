import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string

# Ensure required NLTK resources are available
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def extractive_summarization(text, num_sentences=2):
    # Tokenize sentences
    sentences = sent_tokenize(text)
    
    # Tokenize words and remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word.lower() for word in word_tokenize(text) if word.lower() not in stop_words and word not in string.punctuation]
    
    # Compute word frequency
    word_frequencies = Counter(words)
    
    # Score sentences based on word frequencies
    sentence_scores = {sentence: sum(word_frequencies.get(word.lower(), 0) for word in word_tokenize(sentence)) for sentence in sentences}
    
    # Select top sentences
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    
    return " ".join(summarized_sentences)

# Sample text for testing
text = "Artificial Intelligence (AI) is transforming various industries, including healthcare, finance, and education. In healthcare, AI assists in diagnosing diseases and predicting patient outcomes. In finance, AI algorithms analyze market trends and detect fraudulent activities. Education benefits from AI-powered personalized learning, enhancing student engagement. Despite its advantages, AI poses ethical concerns, such as bias in decision-making and data privacy risks. As AI continues to evolve, it is crucial to develop regulations ensuring responsible use."

# Summarize the text
summary = extractive_summarization(text, num_sentences=2)
print("Summary:", summary)
