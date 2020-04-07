import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib


def predict(data):
    df= pd.read_csv("YoutubeSpamMergedData.csv")
    df_data = df[["CONTENT","CLASS"]]
    # Features and Labels
    df_x = df_data['CONTENT']
    df_y = df_data.CLASS
    # Extract Feature With CountVectorizer
    corpus = df_x
    cv = CountVectorizer()
    X = cv.fit_transform(corpus) # Fit the Data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, df_y, test_size=0.33, random_state=42)
    #Naive Bayes Classifier
    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB()
    clf.fit(X_train,y_train)
    clf.score(X_test,y_test)
    #Alternative Usage of Saved Model
    ytb_model = open("naivebayes_spam_model.pkl","rb")
    clf = joblib.load(ytb_model)

    #comment = request.form['comment']
    data = [data]
    vect = cv.transform(data).toarray()
    my_prediction = clf.predict(vect)

    #print(my_prediction)
    return my_prediction


#predict("nice, check this out")
