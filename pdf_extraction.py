import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text("text") + "\n"
        return text.strip() if text.strip() else "Error: No text found in the PDF."
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage:
#pdf_path = input("Enter the path to texithe PDF file:\n")
pdf_path = "/Users/tahirsmacbok/Downloads/Sample_1.pdf"

extracted_text = extract_text_from_pdf(pdf_path)
print("\nExtracted Text:\n", extracted_text)
