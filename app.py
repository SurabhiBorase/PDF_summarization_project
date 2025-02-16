from flask import Flask, render_template, request
import os
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
from collections import Counter
import string

nltk.download('punkt')

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
            return text.strip()
    except Exception as e:
        return f"Error: {e}"

def extractive_summarization(text, num_sentences=3):
    sentences = sent_tokenize(text)
    words = text.lower().translate(str.maketrans("", "", string.punctuation)).split()
    word_freq = Counter(words)
    
    sentence_scores = {sentence: sum(word_freq[word.lower()] for word in sentence.split()) for sentence in sentences}
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    return " ".join(top_sentences)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'pdf_file' not in request.files:
        return "No file part"
    
    file = request.files['pdf_file']
    if file.filename == '':
        return "No selected file"
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        extracted_text = extract_text_from_pdf(filepath)
        summary = extractive_summarization(extracted_text)
        return render_template('result.html', extracted_text=extracted_text, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
