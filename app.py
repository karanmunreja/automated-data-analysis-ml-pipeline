from dataset_insights import DatasetAnalyzer, ProblemDetector
from preprocessing import DataPreprocessor
from ML_models import RegressionModel, ClassificationModel, ClusteringModel
from recommendations import InsightGenerator

analyzer=DatasetAnalyzer('data/Iris.csv')
summary=analyzer.get_summary()
problem_detection=ProblemDetector().problems
print(problem_detection)
choice=int(input("Enter the problem type you want to solve: 1-4\n"))
problem_type=problem_detection.get(choice)
preprocessor=DataPreprocessor()

if choice in [1,2]:
    X_train,X_test,y_train,y_test=preprocessor.preprocess('data/Iris.csv',problem_type)
    target=X_train.columns[-1]
    if problem_type=='Regression':
       reg_model=RegressionModel(X_train,y_train,X_test,y_test)
       model1,score1=reg_model.regression_model()
       model2,score2=reg_model.knn_regression()
       print(f"Linear Regression Score: {score1}")
       print(f"KNN Regression Score: {score2}")
       models={
              'Linear Regression': (model1,score1),
              'KNN Regression': (model2,score2)
       }
       best_model_name=max(models, key=lambda x: models[x][1])
       best_model,best_score=models[best_model_name]
       insight_generator=InsightGenerator()
       print(f"Best Model: {best_model_name} with a score of {best_score:.2f}")
       insight,recommendation=insight_generator.regression_insights_recommendation(
           best_model,X_train.columns,target
       ) 
       print(f"Insight:{insight}")
       print(f"Recommendation:{recommendation}")
    elif problem_type=='Classification':
        class_model=ClassificationModel(X_train,y_train,X_test,y_test)
        model3,score3=class_model.logistic_regression()
        model4,score4=class_model.Knn_classification()
        print(f"Logistic Regression Score :{score3}")
        print(f"KNN Classification Score :{score4}")
        models={
              'Logistic Regression': (model3,score3),
              'KNN Classification': (model4,score4)
       }
        best_model_name=max(models, key=lambda x: models[x][1])
        best_model,best_score=models[best_model_name]
        insight_generator=InsightGenerator()
        print(f"Best Model: {best_model_name} with a score of {best_score:.2f}")
        insight,recommendation=insight_generator.classification_insights_recommendation(
           best_model,X_train.columns,target
       ) 
        print(f"Insight:{insight}")
        print(f"Recommendation:{recommendation}")

elif choice==3:
    X_train,X_test=preprocessor.preprocess('data/Iris.csv',problem_type)
    cluster_model=ClusteringModel(X_train,X_test)
    model5,score5=cluster_model.KMeans_clustering()
    print(f"KMeans Clustering Score: {score5}")
else:
    print("Invalid choice. Please select a valid problem type.")

#print(summary)
