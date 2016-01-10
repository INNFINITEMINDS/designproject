import numpy as np

def make_prediction(data, labels):

	from sklearn.svm import SVC
	clf = SVC()

	#clf fit not required
	SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)

	pred = clf.predict(data)

	print(pred)


    #clf.score(data, labels)

