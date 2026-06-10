from core.ML_models import *
import time
import streamlit as st

def train_models(problem_type,X_train,X_test=None,y_train=None,y_test=None):
    results     = {}
    score_label = "Score"
    best_k=None

    if problem_type == "Regression":
        prog   = st.progress(0, text="Training Linear Regression…")
        reg    = RegressionModel(X_train, y_train, X_test, y_test)
        m1, s1 = reg.linear_regression()
        results["Linear Regression"] = (m1, s1)
        prog.progress(50, text="Training KNN Regression…")
        m2, s2 = reg.Knn_regression()
        results["KNN Regression"] = (m2, s2)
        prog.progress(100, text="Done!")
        score_label = "R² Score"

    elif problem_type == "Classification":
        prog   = st.progress(0, text="Training Logistic Regression…")
        clf    = ClassificationModel(X_train, y_train, X_test, y_test)
        m1, s1 = clf.logistic_regression()
        results["Logistic Regression"] = (m1, s1)
        prog.progress(50, text="Training KNN Classifier…")
        m2, s2 = clf.Knn_classification()
        results["KNN Classification"] = (m2, s2)
        prog.progress(100, text="Done!")
        score_label = "Accuracy"

    else:
        prog   = st.progress(0, text="Training KMeans Clustering…")
        clu    = ClusteringModel(X_train)
        m1, s1,best_k = clu.KMeans_clustering()
        results["KMeans Clustering"] = (m1, s1)
        prog.progress(100, text="Done!")
        score_label = "Silhouette"

    time.sleep(0.2)
    return results,score_label,best_k