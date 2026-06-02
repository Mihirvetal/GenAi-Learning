# # Stemming is a text preprocessing technique that reduces words to their base or root form by aggressively chopping off common prefixes and suffixes (like "-ing", "-ed", or "-ly").

# from nltk.stem import PorterStemmer 
# # stemming 
# # sentence = "hello i am walking towards from going to doing"
# sentence = ["hello" , "i" ,"am", "walking", "towards", "from", "going", "to" ,"doing"]
# stemming=PorterStemmer()
# for s in sentence:
    
#     print(stemming.stem(s))
    
# # output 
# # hello
# # i
# # am
# # walk
# # toward
# # from
# # go
# # to
# # do

# # lancaster stemming algorithm

# from nltk.stem import LancasterStemmer

# lanc =LancasterStemmer()

# for s in sentence:
#     print(s+ "-->"+ lanc.stem(s))
    
# # output
# # hello-->hello
# # i-->i
# # am-->am
# # walking-->walk
# # towards-->toward
# # from-->from
# # going-->going
# # to-->to
# # doing-->doing



# # lemmatization 
# import nltk
# from nltk.stem import WordNetLemmatizer
# lem = WordNetLemmatizer()
# # nltk.download('wordnet')

# for word in sentence:
#     print(word + "-a-> " + lem.lemmatize(word,pos='v'))



# # Sentiment analysis
# # lemmatize will use in the chatbot




# =====================================================================
# NLP TEXT PREPROCESSING: STEMMING VS. LEMMATIZATION
# =====================================================================
# Stemming reduces words to their base/root form by aggressively chopping 
# off common prefixes and suffixes (like "-ing", "-ed", or "-ly"). 
# It is fast but can result in non-dictionary words.

import nltk
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer

# You only need to run these downloads once in your environment
# nltk.download('wordnet')
# nltk.download('omw-1.4') # Often required by NLTK alongside wordnet

# The raw input tokens (words)
sentence = ["hello", "i", "am", "walking", "towards", "from", "going", "to", "doing"]

# =====================================================================
# 1. PORTER STEMMER
# Extra Info: This is the industry standard, gentle stemming algorithm. 
# It uses a predefined set of 5 sequential rules to strip suffixes.
# Best used for: General search engines or indexing large document bases 
# where exact spelling matters less than grouping similar root words.
# =====================================================================
print("--- PORTER STEMMER ---")
porter = PorterStemmer()

for s in sentence:
    # Using f-strings with spacing (s:10) to make the console output align cleanly
    print(f"{s:10} --> {porter.stem(s)}")

# Expected output:
# walking    --> walk
# towards    --> toward
# going      --> go

# =====================================================================
# 2. LANCASTER STEMMER
# Extra Info: This is a much more aggressive and faster algorithm.
# It can severely chop words down, which reduces vocabulary size 
# significantly but often creates heavily distorted, non-dictionary words.
# Best used for: Applications where speed is the absolute highest priority 
# over readability.
# =====================================================================
print("\n--- LANCASTER STEMMER ---")
lancaster = LancasterStemmer()

for s in sentence:
    print(f"{s:10} --> {lancaster.stem(s)}")

# =====================================================================
# 3. WORDNET LEMMATIZER
# Extra Info: Unlike stemming, Lemmatization uses a massive linguistic 
# database (WordNet) to find the actual dictionary root (the "lemma").
# It requires a Part of Speech (POS) tag to work perfectly. Here, passing 
# pos='v' tells the algorithm to treat every word as a Verb.
# =====================================================================
print("\n--- WORDNET LEMMATIZER ---")
lemmatizer = WordNetLemmatizer()

for word in sentence:
    # Notice how "am" correctly becomes "be". 
    # Stemmers cannot do this because they don't understand actual grammar!
    print(f"{word:10} -a-> {lemmatizer.lemmatize(word, pos='v')}")

# =====================================================================
# REAL-WORLD USE CASES (Building on your notes)
# =====================================================================
# 1. Chatbots / Conversational AI:
# You are completely right—Lemmatization is essential here. If a user 
# types "I am feeling worse", a bot needs to lemmatize "worse" to its root 
# "bad" to correctly trigger an empathetic response. A crude stemmer 
# wouldn't know how to handle irregular words.
#
# 2. Sentiment Analysis:
# Stemming can accidentally chop off letters that change the context of 
# a word entirely. Lemmatization is much safer for preserving the exact 
# emotional tone in product reviews or text classification.