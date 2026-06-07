class InsightGenerator:
    def regression_insights_recommendation(self,model,features,target):
        coefficients=model.coef_
        max_index=coefficients.argmax()
        feature=features[max_index]
        coefficient=coefficients[max_index]
        if coefficient > 0:
            insight=(
                f"The feature '{feature}' has the most positive impact on {target} with a coefficient of {coefficient:.2f}."
            )
            recommendation=f"To increase {target}, focus on increasing '{feature}' as it has the strongest positive influence."
        else:
            insight=(
                f"The feature '{feature}' has the most negative impact on {target} with a coefficient of {coefficient:.2f}."
            )
            recommendation=f"To increase {target}, focus on decreasing '{feature}' as it has the strongest negative influence."
        return insight, recommendation
    
    def classification_insights_recommendation(self,model,features,target):
        importances = abs(model.coef_).mean(axis=0)
        max_index=importances.argmax()
        feature=features[max_index]
        importance=importances[max_index]
        insight=(
            f"The feature '{feature}' is the most important for predicting {target} with an importance score of {importance:.2f}."
        )
        recommendation=f"To improve predictions for {target}, focus on the feature '{feature}' which has the highest importance."
        return insight, recommendation
    
    def clustering_insights_recommendation(self,model,features):
        centers=model.cluster_centers_
        max_value=centers.max()
        cluster_index, feature_index = (
        (centers == max_value).nonzero()
        )
        cluster=cluster_index[0]
        feature=features[feature_index[0]]
        insight=(
            f"The feature '{feature}' has the highest value in cluster {cluster} with a value of {max_value:.2f}."
        )
        recommendation=f"Analyze the cluster {cluster} because it stands out significantly in feature {feature}."
        return insight, recommendation
