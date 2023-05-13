import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Get the sentiment score for a sentence
text = "What are you talking about?"
score = sia.polarity_scores(text)

# Print the sentiment score
print(score['neg'])