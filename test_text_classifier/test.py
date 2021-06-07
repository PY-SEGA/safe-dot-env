# hello Mohammads and Rawan -- use poetry add alt-profanity-check 
from pickle import STRING
from numpy import number, string_
import re
from profanity_check import predict, predict_prob

print(predict(['predict() takes an array and returns a 1 for each string if it is offensive, else 0.']))
# [0]

print(predict(['fuck you']))
# [1]

y = predict_prob(['predict_prob() takes an array and returns the probability each string is offensive'])
print(y)
# [0.03944098]

x = predict_prob(['go to hell, you scum'])
print(x)
# [0.99780641]

print("you smell like a dog",predict(['you smell like a dog']))
# [1]

print(predict_prob(["hearing Freddy Benson swear = ruined childhood"]))
# [0.02898408]


#########################################
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
predict_results=classifier.predict(My_sentences)

vectorizer.transform(sentences).toarray()
predict_results=classifier.predict(My_sentences)
for i in range(len(predict_results)) :
    if predict_results[i] == 1:
        print(f'{sentence[i]} is a good feedback')
    else:
        print(f'{sentence[i]} is a bad feedback')
print(predict_results)


# from pickle import STRING
# from numpy import number, string_
# import re
# from profanity_check import predict, predict_prob
print(predict_prob(['go to hell, you scum']))
def text_classifier(text_test):

    text_predict=[]
    bad_words=[]

    for line in text_test:
        print(predict([line]),'\n\n*************\n')
        print(bad_word_counter(line),'\n\n*************\n')
        text_predict.append(predict([line]))
        bad_words.append(bad_word_counter(line))

    return {"text_predict":text_predict,"bad_words":bad_words}



def bad_word_counter(text_test):
    y = re.findall("([A-z]{1})?\*+", text_test)
    return len(y)



text_classifier(['fuck you\n',"connectivity is an amazing thing by now we're all used to the instant connectivity the puts the world at our fingertips from desktop or devices we can purchase post pin and pick anything anywhere we are connected to the world and each other like never before but how does it happen how does data get from here to there how do different devices and applications connect with each other to allow us to place an order make a reservation or book a flight with just a few %HESITATION son hero of our connect.\n", 'in programming.\n', "or API it's the engine under the hood and is behind the scenes that we take for granted but it's what makes possible all the interactivity we've come to expect and rely upon but exactly what is an A. P. I. question everyone asks okay not really but we're glad you did the textbook definition goes something like this in computer programming and application programming interface A. P. I. is that routines for all.\n", "okay to speak plainly and A. P. I. is the messenger the takes requests and tells the system what you want to do and then returns the sponsor back to you to give you a familiar example think of an API as a waiter in a restaurant imagine you're sitting at the table with a menu choices.\n", "the kitchen is the part of the system which will prepare your order what's missing is the critical link to communicate your order to the kitchen and deliver your food back to your table that's where the waiter for CPI comes in.\n",'fuck you\n', "the waiter is the fuck you messenger but takes your request order and tells the system in this case the kitchen what to do and then delivers a response back to you in this case food now that fuck you we've waited your appetite let's apply this to a real A. P. I. example you are probably familiar with the process of searching for airline flights online just like at a restaurant you have a menu of options to choose from a drop down menu in this case you choose a departure city and date or return city and state cabin class and other variables in order to book your flight you interact with the airlines website to access the fuck you airlines database to see if any seats are available on those dates and what the cost might be based on certain variables but what if you're not using the airlines website which has direct access to the information what if you are using an online travel service that aggregates information from many different airlines I travel service interacts with the airlines API the API is the interface that like your help away %HESITATION can be asked by that online travel service to get information from the airline system over the internet to box seats choose mail preferences for baggage options it also then takes the airlines response to request and delivers it right back to the online travel service which then shows it to you so you can see that it's a P. eyes that make it possible for us all to use travel sites the same goes for all interactions between applications data and devices they all have a P. eyes that allow computers to operate them and that's what ultimately creates connectivity so whenever you think of an API just think of it as your waiter running back and forth between applications databases and devices to deliver data and create the connectivity that puts the world at our fingertips and when ever you think of creating an API thank you all soft.\n",'fuck you\n'])