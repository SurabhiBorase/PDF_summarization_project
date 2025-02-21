from transformers import pipeline

# Load the pre-trained BART model for summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=150, min_length=50):
    """
    Generates an abstractive summary using BART.

    Parameters:
    - text (str): The input text to summarize.
    - max_length (int): Maximum length of the summary.
    - min_length (int): Minimum length of the summary.

    Returns:
    - str: The summarized text.
    """
    if len(text.split()) < min_length:
        return "Input text is too short for summarization."

    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

# 🛠️ TEST BLOCK
if __name__ == "__main__":
    test_text = """
    The advancements in artificial intelligence have revolutionized multiple industries. 
    AI models are now capable of performing complex tasks such as medical diagnosis, 
    financial forecasting, and even creative writing. Companies are investing heavily in 
    AI research to enhance automation and efficiency. However, ethical concerns regarding 
    AI biases and job displacement continue to be widely discussed.
    """
    
    print("\n📝 Original Text:\n", test_text)
    summary = summarize_text(test_text)
    print("\n📌 Generated Summary:\n", summary)
