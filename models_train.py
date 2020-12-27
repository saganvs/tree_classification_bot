from __future__ import division
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pickle

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

data = pd.read_csv("./allrus.csv")
#You don't need those features
data = data.drop(['Mode','Vertical_symmetry','Horizontal_symmetry', 'Minimal_peak'], axis=1)
### getting Xs and Ys #####
X = data.iloc[0:data.shape[0], 1:data.shape[1]]
y = data.iloc[0:data.shape[0], 0]
y = y.astype('category')
classes = np.unique(y)

### NORMALIZATION #######
X_scaled = (X-X.min())/(X.max()-X.min())

### SPLITTING INTO TRAIN AND TEST DATA
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=34)

models = [(KNeighborsClassifier(n_neighbors=13), 'KNN'),
          (SVC(gamma=0.82, C=1, random_state=34), 'SVC'),
          (DecisionTreeClassifier(criterion='entropy',max_depth=11, random_state=34), 'DTC'),
          (RandomForestClassifier(criterion='entropy', max_depth=20, random_state=34), 'RFC'),
          (GaussianNB(), 'GNB')]
          
for m, name in models:
    m.fit(X_scaled, y)
    pickle.dump(m, open(f'RUmodel_{name}.sav', 'wb'))