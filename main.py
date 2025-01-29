import numpy as np
import sqlite3
import os
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier, MLPRegressor  # Import MLP classes
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder  # For handling string labels in MLPClassifier
from scirknn import sklearn2rknn
import jieba
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

# --- CLASSIFICATION with MLPClassifier ---

# 1. Label Encode the string labels
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# 2. Choose and initialize the MLPClassifier
clf = MLPClassifier(hidden_layer_sizes=(100,), max_iter=300, random_state=42,activation='relu') # You can tune hidden_layer_sizes, max_iter, etc
clf.fit(X_train, y_train_encoded)


# 3. Predict using the MLPClassifier and evaluate
y_pred_encoded = clf.predict(X_test)
y_pred = label_encoder.inverse_transform(y_pred_encoded)
accuracy = accuracy_score(y_test, y_pred)
print("分類模型準確度 (MLPClassifier):", accuracy)


# --- REGRESSION with MLPRegressor (if labels are numeric or can be encoded as such) ---
# If your labels were numeric from the beginning you could skip encoding steps and use regressor, and comment out the steps above
# If not we are not able to run regression part
'''
# 1. Use the same or new data split
# X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.8, random_state=42) # If you are not using the previous split

try:
    y_train_numeric = np.array(y_train, dtype=float)
    y_test_numeric = np.array(y_test, dtype=float)

    # 2. Choose and initialize the MLPRegressor
    regressor = MLPRegressor(hidden_layer_sizes=(100,), max_iter=300, random_state=42) # You can tune hidden_layer_sizes, max_iter, etc
    regressor.fit(X_train, y_train_numeric)

    # 3. Predict using the MLPRegressor and evaluate
    y_pred_regressor = regressor.predict(X_test)
    mse = mean_squared_error(y_test_numeric, y_pred_regressor)
    print("迴歸模型均方誤差 (MLPRegressor):", mse)
except ValueError:
    print('can not make regressor')
'''
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
    sklearn2rknn.convert(clf, "clf.rknn", "rk3566", quantization=False)

# 預測未知的科目
while True:
    new_data = [input('預測科目模型測試:')]
    new_data_vectorized = vectorizer.transform(new_data)
    predicted_subject_encoded = clf.predict(new_data_vectorized)
    predicted_subject = label_encoder.inverse_transform(predicted_subject_encoded)
    print(predicted_subject)