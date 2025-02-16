import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
from collections import Counter
import string

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

# Main Execution
pdf_path = input("Enter the path to the PDF file: ").strip().strip("'\"")
extracted_text = extract_text_from_pdf(pdf_path)

if extracted_text:
    print("\nExtracted Text:\n", extracted_text)
    summary = extractive_summarization(extracted_text, num_sentences=3)
    print("\nSummary:\n", summary)
else:
    print("Failed to extract text from the PDF.")

import PyPDF2

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""  # Handle None values
            return text.strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

pdf_path = input("Enter the path to the PDF file: ").strip()
text = extract_text_from_pdf(pdf_path)

if text:
    print("\nExtracted Text:\n", text)
else:
    print("\nFailed to extract text from the PDF. Check if it's scanned or encrypted.")

