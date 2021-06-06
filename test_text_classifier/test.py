# hello Mohammads and Rawan -- use poetry add alt-profanity-check 
from profanity_check import predict, predict_prob

print(predict(['predict() takes an array and returns a 1 for each string if it is offensive, else 0.']))
# [0]

print(predict(['fuck you']))

# [1]

y = predict_prob(['predict_prob() takes an array and returns the probability each string is offensive'])
print(y)
# [0.08686173]

x = predict_prob(['go to hell, you scum'])
print(x)

print(predict(['you smell like a dog']))
# [0.7618861]
print(predict_prob(["hearing Freddy Benson swear = ruined childhood"]))



# ########################################

import pandas as pd

filepath_dict = {'yelp':   'data/yelp_labelled.txt',
                 'amazon': 'data/amazon_cells_labelled.txt',
                 'imdb':   'data/imdb_labelled.txt'}

df_list = []
for source, filepath in filepath_dict.items():
    df = pd.read_csv(filepath, names=['sentence', 'label'], sep='\t')
    df['source'] = source  
    df_list.append(df)

df = pd.concat(df_list)

sentences = ['John likes ice cream', 'John hates chocolate.']

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(min_df=0, lowercase=False)
vectorizer.fit(sentences)
transformed = vectorizer.transform(sentences).toarray()
from sklearn.model_selection import train_test_split
df_yelp = df[df['source'] == 'yelp']

sentences = df_yelp['sentence'].values
y = df_yelp['label'].values

sentences_train, sentences_test, y_train, y_test = train_test_split(
   sentences, y, test_size=0.25, random_state=1000)


vectorizer = CountVectorizer()
vectorizer.fit(sentences_train)

X_train = vectorizer.transform(sentences_train)
X_test  = vectorizer.transform(sentences_test)

from sklearn.linear_model import LogisticRegression

# S shape sigmoid   
#.       ______
#.      |
#  _____

classifier = LogisticRegression()
classifier.fit(X_train, y_train)
score = classifier.score(X_test, y_test)

print("Accuracy:", score)

sentence = ['I love playing this course','I hate this course bad','this course is bad']
My_sentences = vectorizer.transform(sentence)
predict=classifier.predict(My_sentences)

vectorizer.transform(sentences).toarray()
predict=classifier.predict(My_sentences)
for i in range(len(predict)) :
    if predict[i] == 1:
        print(f'{sentence[i]} is a good feedback')
    else:
        print(f'{sentence[i]} is a bad feedback')
print(predict)
