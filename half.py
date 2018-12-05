import sklearn as sk
from sklearn.svm import LinearSVC
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier

data = pd.read_csv("Data3.csv", index_col=0)
# drop release date because not numeric
data = data.drop(columns = ["Album Release Date"])

# set NaN values to average sentiment
sentiment = data["Sentiment"]
average_sentiment = sentiment.mean()
i = 0
for s in sentiment:
    if pd.isna(s):
        data.set_value(i, "Sentiment", average_sentiment)
    i += 1

# replace #VALUE! with average year
years = data["Year"]
i = 0
for year in years:
    try:
        data.set_value(i, "Year", float(year))
    except ValueError:
        print year
        data.set_value(i, "Year", 0)
    i += 1
average_year = years.mean()
i = 0
for year in years:
    if year == 0:
        data.set_value(i, "Year", average_year)
    i += 1

# data with less features
data2 = pd.concat([data["Popularity"], data["Half"], data["Sentiment"]], axis=1)
data2.columns = ["Popularity", "Half", "Sentiment"]

# features and labels
X = data.drop(columns=["Half"])
Y = data["Half"]

# perform k folds cross validation
kf = KFold(n_splits = 10, shuffle=True)
kf.get_n_splits(X)

# average accuracy
score = 0.

# loop through splits
for train_index, test_index in kf.split(X):
    # separate training and testing data
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    Y_train, Y_test = Y.iloc[train_index], Y.iloc[test_index]
    
    # LinearSVC
    clf = LinearSVC()
    # k nearest neighbors
    #n_neighbors = 70
    #clf = sk.neighbors.KNeighborsClassifier(n_neighbors, weights='uniform')
    # neural network
    #clf = MLPClassifier(solver="lbfgs", alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    # fit the model on training data
    clf.fit(X_train, Y_train)
    # update average score
    score += clf.score(X_train, Y_train)/10

print score
    
