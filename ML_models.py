from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.cluster import KMeans

class RegressionModel:
    def __init__(self,X_train,y_train,X_test,y_test):
        self.X_train=X_train
        self.y_train=y_train
        self.X_test=X_test
        self.y_test=y_test

    def linear_regression(self):
        Linear_Regression=LinearRegression()
        Linear_Regression.fit(self.X_train,self.y_train)
        score=Linear_Regression.score(self.X_test,self.y_test)
        return Linear_Regression,score
    def Knn_regression(self):
        KNN_regressor=KNeighborsRegressor()
        KNN_regressor.fit(self.X_train,self.y_train)
        score=KNN_regressor.score(self.X_test,self.y_test)
        return KNN_regressor,score
    
class ClassificationModel:
    def __init__(self,X_train,y_train,X_test,y_test):
        self.X_train=X_train
        self.y_train=y_train
        self.X_test=X_test
        self.y_test=y_test

    def logistic_regression(self):
        Logistic_Regression=LogisticRegression()
        Logistic_Regression.fit(self.X_train,self.y_train)
        score=Logistic_Regression.score(self.X_test,self.y_test)
        return Logistic_Regression,score
    def Knn_classification(self):
        KNN_classifier=KNeighborsClassifier()
        KNN_classifier.fit(self.X_train,self.y_train)
        score=KNN_classifier.score(self.X_test,self.y_test)
        return KNN_classifier,score

class ClusteringModel:
    def __init__(self,X_train,X_test):
        self.X_train=X_train
        self.X_test=X_test
        
    def KMeans_clustering(self):
        KMeans_cluster=KMeans()
        KMeans_cluster.fit(self.X_train)
        score=KMeans_cluster.inertia_
        return KMeans_cluster,score