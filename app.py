import gradio as gr
import re

def summarize_text(text):
    if not text.strip():
        return "Please enter some text."

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    if len(sentences) <= 2:
        return text

    # Simple extractive summarization
    words = re.findall(r'\b\w+\b', text.lower())

    stop_words = {
        "the", "is", "a", "an", "and", "of", "to", "in",
        "on", "for", "with", "that", "this", "are", "was",
        "as", "by", "it", "from"
    }

    word_frequency = {}

    for word in words:
        if word not in stop_words:
            word_frequency[word] = word_frequency.get(word, 0) + 1

    sentence_scores = {}

    for sentence in sentences:
        score = 0
        for word in re.findall(r'\b\w+\b', sentence.lower()):
            score += word_frequency.get(word, 0)

        sentence_scores[sentence] = score

    # Select top 30% sentences
    number_of_sentences = max(1, round(len(sentences) * 0.3))

    important_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:number_of_sentences]

    # Keep original order
    summary = [
        sentence for sentence in sentences
        if sentence in important_sentences
    ]

    return " ".join(summary)


demo = gr.Interface(
    fn=summarize_text,
    inputs=gr.Textbox(
        lines=12,
        placeholder="Enter your text here..."
    ),
    outputs=gr.Textbox(
        lines=8,
        label="Summary"
    ),
    title="NLP Text Summarization System",
    description="Enter a paragraph or article and get an extractive summary."
)

demo.launch()
