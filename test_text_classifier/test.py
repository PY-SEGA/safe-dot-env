# hello Mohammads and Rawan -- use poetry add alt-profanity-check 
from pickle import STRING
from numpy import number, string_
import re
from profanity_check import predict, predict_prob


#########################################
import pandas as pd
import pysnooper


filepath_dict = {'yelp':   'data/yelp_labelled.txt',
                 'amazon': 'data/amazon_cells_labelled.txt',
                 'imdb':   'data/imdb_labelled.txt'}

df_list = []
for source, filepath in filepath_dict.items():
    df = pd.read_csv(filepath, names=['sentence', 'label'], sep='\t')
    df['source'] = source  
    df_list.append(df)

df = pd.concat(df_list)


from sklearn.feature_extraction.text import CountVectorizer

from sklearn.model_selection import train_test_split

sentences = df['sentence'].values
y = df['label'].values

sentences_train, sentences_test, y_train, y_test = train_test_split(
   sentences, y, test_size=0.25, random_state=1000)
vectorizer = CountVectorizer()
vectorizer.fit(sentences_train)

X_train = vectorizer.transform(sentences_train)
X_test  = vectorizer.transform(sentences_test)

from sklearn.linear_model import LogisticRegression

classifier = LogisticRegression()
classifier.fit(X_train, y_train)
score = classifier.score(X_test, y_test)

# print("Accuracy:", score)

# sentence = ['I love playing this course','I hate this course bad','this course is bad']
def comments_test(comments_list):
    My_sentences = vectorizer.transform(comments_list)
    predict_results=classifier.predict(My_sentences)

    vectorizer.transform(sentences).toarray()
    predict_results=classifier.predict(My_sentences)
    # print(predict_results)
    good = 0
    bad = 0
    for i in range(len(predict_results)) :
        if predict_results[i] == 1:
            good+=1
        else:
            bad+=1
    return {'bad_comments':good/(len(comments_list)) , 'good_comments':bad/(bad+good)}


# from pickle import STRING
# from numpy import number, string_
# import re
# from profanity_check import predict, predict_prob
# print(predict(['go to hell, you scum']))
# subtitle_list
def bad_word_counter(text_test):
    y = re.findall("([A-z]{1})?\*+", text_test)
    return len(y)


def bad_words_by_line(text_test):
    bad_arr = []
    for line in text_test:
        y = re.findall("([A-z]{1})?\*+", line)
        if len(y) > 0:
            bad_arr.append(1)
    return bad_arr

# @pysnooper.snoop()
def text_classifier(text_test):
    text_predict=[]
    bad_words=[0]
    if len(text_test): 
        for line in text_test:
            text_predict.append(predict([line])[0])
            # print(text_predict, 'this is line')
            bad_words.append(bad_word_counter(line))
        text_predict=(sum(text_predict)+ len(bad_words_by_line(text_test)))/len(text_test)
        # print(sum(text_predict), 'sum text')
        # print(len(text_test), 'length')
        # print(len(bad_words_by_line(text_test)), 'bad_text55')
    else:
        text_predict = 0
    return {"text_predict":text_predict,"bad_words":sum(bad_words)}

print(text_classifier(['Its your turn baby', ' seconds Let this motherfucker feel it', 'Alright DJ spin that shit', 'Come on Rabbit', 'Dont choke this time', 'All right look', 'Hey yo', 'This guy raps like his parents jerked him', 'He sounds like Erick Sermon the generic version', 'This whole crowd looks suspicious Its all dudes here except for these bitches', 'So Im a German eh Thats okay You look like a fuckin worm with braids', 'These Leaders of the Free World rookies Lookie how can six dicks be pussies', 'Talkin about shits creek Bitch you could be up piss creek with paddles this deep', 'Youre still gonna sink Youre a disgrace', 'Yeah they call me Rabbit This is a turtle race', 'He cant get with me spitting this shit', 'Wickedly lickety shot suspicious spickety split lickety', 'Now Im gonna turn around with a great smile And walk my white ass back across  Mile', ' You cant fuck with us', 'Come on Rabbit', 'Ward I think you were a little hard on the Beaver', 'So was Eddie Haskell Wally and Ms Cleaver', 'This guy keeps screamin hes paranoid Quick someone get his ass another steroid', 'Blahbadibooblah bahbadiblooblah', 'I aint hear a word you said Hippity hoopla', 'Is that a tanktop or a new bra Look Snoop Dogg just got a fuckin boobjob', 'Didnt you listen to the last round meathead Pay attention youre sayin the same shit that he said', 'Matter of fact dawg heres a pencil', 'Go home write some shit make it suspenseful', 'And dont come back until somethin dope hits you', 'Fuck it you can take the mic home with you', 'Lookin like a cyclone hit you', 'Tanktop screamin Lotto I dont fit you', 'You see how far the white jokes get you Boys like How Vanilla Ice gon diss you', 'My motto Fuck Lotto', 'I get the seven digits from your mother for a dollar tomorrow', 'Now everybody from the ', 'Put your motherfucking hands up and follow me', 'Everybody from the  Put your motherfucking hands up', 'Look look', 'Now while he stands tough Notice that this man did not have his hands up', 'This Free Worlds got you gassed up Now whos afraid of the Big Bad Wolf', 'One two three and to the four One Pac two Pac three Pac four', 'Four Pac three Pac two Pac one Youre Pac hes Pac no Pac none', 'This guy aint no motherfucking MC', 'I know everything hes bout to say against me', 'I am white I am a fucking bum I do live in a trailer with my mom', 'My boy Future is an Uncle Tom I do got a dumb friend named Cheddar Bob', 'Who shoots himself in his leg with his own gun', 'I did get jumped by all six of you chumps', 'And Wink did fuck my girl Im still standing here screaming Fuck the Free World', 'Dont ever try to judge me dude You dont know what the fuck Ive been through', 'But I know something about you You went to Cranbrook thats a private school', 'Whats the matter dawg You embarrassed This guys a gangster His real names Clarence', 'And Clarence lives at home with both parents And Clarence parents have a real good marriage', 'This guy dont wanna battle hes shook', 'Cause aint no such things as halfway crooks', 'Hes scared to death hes scared to look At his fucking yearbook fuck Cranbrook', '[Music cuts out]', 'Fuck a beat Ill go a cappella', 'Fuck a Papa Doc fuck a clock fuck a trailer Fuck everybody Fuck yall if you doubt me', 'Im a piece of fucking white trash I say it proudly', 'And fuck this battle I dont wanna win Im outtie', 'Here tell these people something they dont know about me', 'Papa Doc what you gonna do', 'DJ A minute and a half Spin that shit', 'We got a new champion', 'BRabbit', 'Lets go', '[Crowd chanting] Fuck Free World ', '[Crowd chanting] BRabbit'])
)



# text_classifier(['fuck you\n',"connectivity is an amazing thing by now we're all used to the instant connectivity the puts the world at our fingertips from desktop or devices we can purchase post pin and pick anything anywhere we are connected to the world and each other like never before but how does it happen how does data get from here to there how do different devices and applications connect with each other to allow us to place an order make a reservation or book a flight with just a few %HESITATION son hero of our connect.\n", 'in programming.\n', "or API it's the engine under the hood and is behind the scenes that we take for granted but it's what makes possible all the interactivity we've come to expect and rely upon but exactly what is an A. P. I. question everyone asks okay not really but we're glad you did the textbook definition goes something like this in computer programming and application programming interface A. P. I. is that routines for all.\n", "okay to speak plainly and A. P. I. is the messenger the takes requests and tells the system what you want to do and then returns the sponsor back to you to give you a familiar example think of an API as a waiter in a restaurant imagine you're sitting at the table with a menu choices.\n", "the kitchen is the part of the system which will prepare your order what's missing is the critical link to communicate your order to the kitchen and deliver your food back to your table that's where the waiter for CPI comes in.\n",'fuck you\n', "the waiter is the fuck you messenger but takes your request order and tells the system in this case the kitchen what to do and then delivers a response back to you in this case food now that fuck you we've waited your appetite let's apply this to a real A. P. I. example you are probably familiar with the process of searching for airline flights online just like at a restaurant you have a menu of options to choose from a drop down menu in this case you choose a departure city and date or return city and state cabin class and other variables in order to book your flight you interact with the airlines website to access the fuck you airlines database to see if any seats are available on those dates and what the cost might be based on certain variables but what if you're not using the airlines website which has direct access to the information what if you are using an online travel service that aggregates information from many different airlines I travel service interacts with the airlines API the API is the interface that like your help away %HESITATION can be asked by that online travel service to get information from the airline system over the internet to box seats choose mail preferences for baggage options it also then takes the airlines response to request and delivers it right back to the online travel service which then shows it to you so you can see that it's a P. eyes that make it possible for us all to use travel sites the same goes for all interactions between applications data and devices they all have a P. eyes that allow computers to operate them and that's what ultimately creates connectivity so whenever you think of an API just think of it as your waiter running back and forth between applications databases and devices to deliver data and create the connectivity that puts the world at our fingertips and when ever you think of creating an API thank you all soft.\n",'fuck you\n'])