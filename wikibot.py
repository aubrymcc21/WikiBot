import wikipediaapi
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from heapq import nlargest

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def fetch_wikipedia_summary(topic):
    wiki_wiki = wikipediaapi.Wikipedia(topic + ' (aubrymcc21@gmail.com)', 'en')
    input_page = wiki_wiki.page(topic)
    if input_page.exists():
        page = wiki_wiki.page(topic)
        print("Going to " + page.canonicalurl)
    else:
        return None
    
    return page.text

def create_summary(text, num_sentences=3):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalnum() and word not in stop_words]

    # Calculate word frequency distribution
    freq_dist = FreqDist(words)

    # Get the most frequent words
    most_common = nlargest(10, freq_dist, key=freq_dist.get)

    # Identify sentences that contain the most frequent words
    summary_sentences = [sent for sent in sentences if any(word in sent.lower() for word in most_common)]

    # Limit the number of summary sentences
    summary_sentences = summary_sentences[:num_sentences]

    return " ".join(summary_sentences)

if __name__ == "__main__":
    topic = input("Enter a Wikipedia topic, or type 'quit' to quit: ")

    while topic != 'quit':
        wiki_summary = fetch_wikipedia_summary(topic)
        if wiki_summary:
            summary = create_summary(wiki_summary)
            print(f"\nSummary of '{topic}':")
            print(summary)
        else:
            print(f"'{topic}' does not exist in Wikipedia. Please search another topic.")
        topic = input("\nEnter a new Wikipedia topic, or type 'quit' to quit: ")
    print("Ending the program...")