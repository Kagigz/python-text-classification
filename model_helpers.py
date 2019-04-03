import text_processing

import pandas as pd
import sklearn
from sklearn import cluster
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score


###########
# TRAINING
###########

# Gets file from Blob Storage and stores it locally
def createDataframe(path):
    data = pd.read_csv(path,sep="|",encoding='utf-8')
    print("Data frame created.")
    return data

# Splits dataset into training and testing data
def split(dataframe):
    train, test = train_test_split(dataframe, test_size=0.33, random_state=42)
    print('Training Data Shape:', train.shape)
    print('Testing Data Shape:', test.shape)
    return train,test

# Creates pipeline
def createPipeline():
    vectorizer = CountVectorizer(tokenizer=text_processing.tokenization)
    clf = LinearSVC()
    pipe = Pipeline([('cleanText', text_processing.CleanTextTransformer()), ('vectorizer', vectorizer), ('clf', clf)])
    return pipe

# Returns accuracy
def getAccuracy(labels,preds):
    return accuracy_score(labels, preds)


#############
# PREDICTIONS
#############

# Returns predicted label for given text
def getPrediction(txt,model):
    testTxt = [txt]
    prediction = model.predict(testTxt)[0]
    print("Prediction: ", prediction)
    return prediction