import sklearn as sk

# Linear SVC
clf = sk.svm.LinearSVC(gamma='scale')
clf.fit(___, ___)
clf.predict(___)

# Nearest Neighbors Classification
n_neighbors = ___
for weights in ['uniform', 'distance']
    clf = sk.neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(___, ___)
    
