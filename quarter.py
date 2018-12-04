import sklearn as sk
from sklearn.svm import LinearSVC
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier

data = pd.read_csv("Data2.csv", index_col=0)
data = data.drop(columns = ["Album Release Date"])

sentiment = data["Sentiment"]
average_sentiment = sentiment.mean()
i = 0
for s in sentiment:
    if pd.isna(s):
        data.set_value(i, "Sentiment", average_sentiment)
    i += 1

data2 = pd.concat([data["Popularity"], data["Quarter"], data["Sentiment"]], axis=1)

data2.columns = ["Popularity", "Quarter", "Sentiment"]

X = data.drop(columns=["Quarter"])
Y = data["Quarter"]

kf = KFold(n_splits = 10, shuffle=True)
kf.get_n_splits(X)

score = 0.

for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    Y_train, Y_test = Y.iloc[train_index], Y.iloc[test_index]
    n_neighbors = 70
    clf = sk.neighbors.KNeighborsClassifier(n_neighbors, weights='uniform')
    #clf = MLPClassifier(solver="lbfgs", alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(X_train, Y_train)
    score += clf.score(X_train, Y_train)/10

print score
