import numpy as np
import sqlite3
import os
# from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import configparser
config = os.environ
import jieba,sys
from joblib import dump, load

con = sqlite3.connect('subject.db')
cur = con.cursor()

cur.execute("SELECT * FROM subjects")

# 讀取資料並處理
data = []
labels = []
for document in cur.fetchall():
    data.append(document[0])
    labels.append(document[1])

# Takes in a document, separates the words
def tokenize_zh(text):
    words = jieba.lcut(text)
    return words

# Add a custom list of stopwords for punctuation
stop_words = ['。', '，']


# 特徵工程，這裡使用Count向量化
vectorizer = CountVectorizer(tokenizer=tokenize_zh,stop_words = stop_words)
X = vectorizer.fit_transform(data)

# 切割數據集
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.8, random_state=42)

# 選擇機器學習算法，這裡使用多類SVM
clf = SVC(kernel='linear', C=1)
clf.fit(X_train, y_train)

# 評估模型
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("模型準確度:", accuracy)

try:
    if sys.argv[1] == 'build':
        dump(clf, 'subject_recognition_model.joblib')
        dump(vectorizer, 'subject_reconition_vec.joblib')
        sys.exit()
except IndexError:
    pass


# 部署模型，可以保存模型以供以後使用
if input('保存模型嗎？請回y \n') == 'y':
    dump(clf, 'subject_recognition_model.joblib')
    dump(vectorizer, 'subject_reconition_vec.joblib')

# 預測未知的科目
while True:
    new_data = [input('預測科目模型測試:')]
    new_data_vectorized = vectorizer.transform(new_data)
    predicted_subject = clf.predict(new_data_vectorized)
    print(predicted_subject)









