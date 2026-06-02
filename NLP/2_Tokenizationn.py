# # will install the library for the Tokenization  #NLTK
# #  do pip install nltk 
# from nltk.tokenize import sent_tokenize 
# import nltk
# # nltk.download('punkt')
# # nltk.download('punkt_tab')
# # paragraph to sentence 
# corpus = """
# Hello my name is Mihir Vetal
# I started learning GenAI.
# NLP is interesting.
# """
# print(sent_tokenize(corpus))
# # paraagraph to words 
# from nltk.tokenize import word_tokenize
# from nltk.tokenize import wordpunct_tokenize
# print(word_tokenize(corpus))
# print(wordpunct_tokenize(corpus))


import nltk
# Ensure you have the necessary datasets downloaded
# nltk.download('punkt')
# nltk.download('punkt_tab')

# Your raw text data (often referred to as a corpus in NLP)
corpus = """
Hello, my name is Mihir Vetal! I'm learning GenAI at 5:00 AM... 
NLP is amazing, isn't it? Check out #AI #NLP learning! :)
"""

# =====================================================================
# 1. SENTENCE TOKENIZATION
# =====================================================================
from nltk.tokenize import sent_tokenize 

# sent_tokenize: Splits a large paragraph/corpus into individual sentences.
# It looks for punctuation cues like periods (.), exclamation marks (!), and question marks (?).
print("--- Sentence Tokenization ---")
print(sent_tokenize(corpus))


# =====================================================================
# 2. WORD TOKENIZATION METHODS
# =====================================================================
from nltk.tokenize import word_tokenize
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import TweetTokenizer

# word_tokenize: The standard, go-to word tokenizer in NLTK.
# It uses the Penn Treebank conventions. It is smart enough to separate contractions 
# like "I'm" into "I" and "'m", and keeps punctuation marks as standalone tokens.
print("\n--- Standard Word Tokenizer ---")
print(word_tokenize(corpus))

# wordpunct_tokenize: Splits text purely based on alphanumeric characters and non-alphanumeric characters.
# It is a simpler, rules-based splitter. For example, it splits contractions and punctuation completely 
# (e.g., "isn't" becomes ['isn', "'", 't'] and "5:00" becomes ['5', ':', '00']).
print("\n--- WordPunct Tokenizer ---")
print(wordpunct_tokenize(corpus))

# TreebankWordTokenizer: The underlying class for word_tokenize.
# It splits contractions (like "isn't" into "is" and "n't") and separates final punctuation,
# but it keeps expressions like fractions or specific sub-words together depending on English grammar rules.
treebank_tokenizer = TreebankWordTokenizer()
print("\n--- Treebank Word Tokenizer ---")
print(treebank_tokenizer.tokenize(corpus))

# RegexpTokenizer: A highly customizable tokenizer where YOU define what a token looks like using Regular Expressions.
# '[\w]+' tells it to match only alphanumeric characters (words/numbers) and completely ignore any punctuation.
regex_tokenizer = RegexpTokenizer(r'[\w]+')
print("\n--- Regexp Tokenizer (Only Words/Numbers, No Punctuation) ---")
print(regex_tokenizer.tokenize(corpus))

# TweetTokenizer: Specifically engineered for social media text (Tweets, chat logs, comments).
# Normal tokenizers break up hashtags (#AI), mentions (@user), and emojis (:) or ;)), making them lose meaning.
# TweetTokenizer keeps hashtags, mentions, and emoticons intact, and can even normalize repeated characters.
tweet_tokenizer = TweetTokenizer(preserve_case=True)
print("\n--- Tweet Tokenizer (Best for Social Media/Chat Data) ---")
print(tweet_tokenizer.tokenize(corpus))