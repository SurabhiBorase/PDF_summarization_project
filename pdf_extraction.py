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
            text = ""
            for page in reader.pages:
                text += page.extract_text() + " "
            return text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def extractive_summarization(text, num_sentences=2):
    sentences = sent_tokenize(text)
    words = text.lower().translate(str.maketrans("", "", string.punctuation)).split()
    word_freq = Counter(words)

    sentence_scores = {sentence: sum(word_freq[word.lower()] for word in sentence.split()) for sentence in sentences}

    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    return " ".join(top_sentences)

def clean_summary(summary):
    """Remove extra spaces, fix spacing issues, and clean the summary output."""
    summary = re.sub(r'\s+', ' ', summary)  # Remove extra spaces and newlines
    summary = summary.strip()
    return summary

# Main Execution
pdf_path = input("Enter the path to the PDF file: ").strip().strip("'\"")
extracted_text = extract_text_from_pdf(pdf_path)

if extracted_text:
    print("\nExtracted Text:\n", extracted_text)
    
    summary = extractive_summarization(extracted_text, num_sentences=3)
    cleaned_summary = clean_summary(summary)  # Apply cleaning function

    print("\nCleaned Summary:\n", cleaned_summary)  # Print cleaned summary
else:
    print("Failed to extract text from the PDF.")
