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
    """Remove extra spaces, fix spacing issues, and clean the summary output."""
    summary = re.sub(r'\s+', ' ', summary)  # Remove extra spaces and newlines
    summary = summary.strip()
    return summary

# Main Execution
pdf_path = input("Enter the path to the PDF file: ").strip().strip("'\"")
num_sentences = int(input("Enter the number of sentences for the summary: ").strip())

extracted_text = extract_text_from_pdf(pdf_path)

if extracted_text:
    print("\nExtracted Text:\n", extracted_text)
    summary = extractive_summarization(extracted_text, num_sentences)
    print("\nCleaned Summary:\n", summary)
else:
    print("Failed to extract text from the PDF.")
