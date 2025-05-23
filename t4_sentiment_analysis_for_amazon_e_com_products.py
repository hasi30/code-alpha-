# -*- coding: utf-8 -*-
"""t4 sentiment analysis for amazon e com products

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KolziAUYedvWsqxnLO3JDgHcJWTOReiD

sentiment analysis for amazon ecom products
"""

pip install pandas numpy nltk textblob matplotlib seaborn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import nltk
nltk.download('punkt')  # Only needed once

# Load your dataset, handling potential errors with 'error_bad_lines' and specifying the 'lines' argument for JSON
# The 'lines' argument treats each line of the file as a separate JSON object
df = pd.read_json("/content/Cell_Phones_and_Accessories_5.json", lines=True)

# Print information about the DataFrame
df.info()

df.head()

# Drop missing values
df = df.dropna(subset=['reviewerID'])

# Basic text cleaning (optional: you can add more)
df['Clean_Review'] = df['reviewText'].str.lower().str.replace(r'[^\w\s]', '', regex=True)

# Function to get polarity and sentiment
def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Apply to cleaned reviews
df['Sentiment'] = df['Clean_Review'].apply(get_sentiment)
df['Polarity'] = df['Clean_Review'].apply(lambda x: TextBlob(x).sentiment.polarity)

sns.countplot(data=df, x='Sentiment', palette='bright')
plt.title("Sentiment Distribution")
plt.show()

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Prepare text
positive_text = ' '.join(df[df['Sentiment'] == 'Positive']['Clean_Review'])
negative_text = ' '.join(df[df['Sentiment'] == 'Negative']['Clean_Review'])

# Generate word clouds
positive_wc = WordCloud(width=800, height=400, background_color='white').generate(positive_text)
negative_wc = WordCloud(width=800, height=400, background_color='black').generate(negative_text)

# Display both with matplotlib
plt.figure(figsize=(16, 8))

plt.subplot(1, 2, 1)
plt.imshow(positive_wc, interpolation='bilinear')
plt.axis('off')
plt.title("✅ Positive Reviews")

plt.subplot(1, 2, 2)
plt.imshow(negative_wc, interpolation='bilinear')
plt.axis('off')
plt.title("❌ Negative Reviews")

plt.show()

# Most positive reviews
top_positive = df.sort_values(by='Polarity', ascending=False).head(5)
print("🔝 Most Positive Reviews:")
print(top_positive[['reviewText', 'Polarity']])

# Most negative reviews
top_negative = df.sort_values(by='Polarity').head(5)
print("\n🔻 Most Negative Reviews:")
print(top_negative[['reviewText', 'Polarity']])

from collections import Counter
import re

# Combine all top reviews into one text
pos_text = ' '.join(top_positive['reviewText'].dropna()).lower()
neg_text = ' '.join(top_negative['reviewText'].dropna()).lower()

# Simple keyword extractor
def extract_keywords(text, stopwords=set()):
    words = re.findall(r'\b\w{4,}\b', text)  # Keep words with 4+ letters
    keywords = [word for word in words if word not in stopwords]
    return Counter(keywords).most_common(10)

# Custom stopwords (add more as needed)
stopwords = set(['product', 'this', 'very', 'have', 'with', 'from', 'good', 'bad'])

# Extract
print("✅ Most common keywords in positive reviews:")
print(extract_keywords(pos_text, stopwords))

print("\n❌ Most common keywords in negative reviews:")
print(extract_keywords(neg_text, stopwords))

import matplotlib.pyplot as plt

# Sample keyword frequencies
pos_keywords = [('excellent', 1), ('punk', 1), ('retro', 1), ('texture', 1),
                ('wonderful', 1), ('idea', 1), ('speak', 1), ('about', 1),
                ('android', 1), ('devices', 1)]

neg_keywords = [('ever', 4), ('worst', 3), ('awful', 2), ('like', 2),
                ('even', 2), ('control', 2), ('cable', 2), ('otterbox', 1),
                ('owned', 1), ('flimsy', 1)]

# Separate into labels and values
pos_words, pos_counts = zip(*pos_keywords)
neg_words, neg_counts = zip(*neg_keywords)

# Plot
fig, axs = plt.subplots(1, 2, figsize=(16, 6))

# Positive reviews
axs[0].barh(pos_words, pos_counts, color='green')
axs[0].set_title("ositive Review Keywords")
axs[0].invert_yaxis()

# Negative reviews
axs[1].barh(neg_words, neg_counts, color='red')
axs[1].set_title("Negative Review Keywords")
axs[1].invert_yaxis()

plt.tight_layout()
plt.show()



