from textblob import TextBlob

text = "I fucking hate you"
blob = TextBlob(text)

polarity = blob.sentiment.polarity  # sentiment polarity (-1 to 1)
subjectivity = blob.sentiment.subjectivity  # sentiment subjectivity (0 to 1)

print("Sentiment polarity:", polarity)
print("Sentiment subjectivity:", subjectivity)