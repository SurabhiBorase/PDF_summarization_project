import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
from collections import Counter
import string
import re

# Ensure required NLTK packages are downloaded
nltk.download('punkt')
nltk.download('stopwords')

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file.

    Parameters:
    - pdf_path (str): Path to the PDF file.

    Returns:
    - str: Cleaned extracted text from the PDF.
    """
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())

            # Remove unnecessary spaces and fix broken words
            text = re.sub(r"\s+", " ", text)  # Remove multiple spaces
            text = re.sub(r"(\w+)-\s(\w+)", r"\1\2", text)  # Fix broken words
            return text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def extractive_summarization(text, num_sentences=3):
    """
    Generates an extractive summary from the input text.

    Parameters:
    - text (str): The input text to summarize.
    - num_sentences (int): Number of sentences to include in the summary.

    Returns:
    - str: Extractive summary.
    """
    sentences = sent_tokenize(text)
    
    # Preprocess text (remove broken words, extra spaces)
    clean_sentences = [" ".join(sentence.split()) for sentence in sentences]

    # Compute word frequency
    words = text.lower().translate(str.maketrans("", "", string.punctuation)).split()
    word_freq = Counter(words)

    # Compute sentence scores (word importance + position boost)
    sentence_scores = {}
    for i, sentence in enumerate(clean_sentences):
        sentence_scores[sentence] = sum(word_freq[word.lower()] for word in sentence.split())

        # Give higher importance to first & last sentences
        if i == 0 or i == len(sentences) - 1:
            sentence_scores[sentence] *= 1.2  

    # Select top sentences
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]

    return " ".join(top_sentences)

def clean_summary(summary):
    """
    Cleans the summary text by removing extra spaces and formatting issues.

    Parameters:
    - summary (str): The summary text to clean.

    Returns:
    - str: Cleaned summary.
    """
    summary = re.sub(r'\s+', ' ', summary)  # Remove extra spaces and newlines
    summary = summary.strip()
    return summary
