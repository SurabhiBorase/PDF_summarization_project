from flask import Flask, render_template, request
from pdf_extraction import extract_text_from_pdf, extractive_summarization
from summarization import summarize_text
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_pdf():
    if request.method == "GET":
        return render_template("upload.html")  # Show the upload page

    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    # Get summarization type from form
    summarization_type = request.form.get("summary_type", "abstractive")  # Default is abstractive
    num_sentences = int(request.form.get("num_sentences", 3))  # Default to 3 sentences for extractive

    if summarization_type == "extractive":
        summary = extractive_summarization(extracted_text, num_sentences)
    else:
        summary = summarize_text(extracted_text)  # Use BART abstractive summarization

    return render_template("result.html", extracted_text=extracted_text, summary=summary)


if __name__ == "__main__":
    app.run(debug=True)
