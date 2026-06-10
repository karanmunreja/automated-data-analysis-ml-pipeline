from core.recommendations import InsightGenerator
from core.recommendations import InsightGenerator

def generate_insights(
    problem_type,
    best_model,
    columns,
    target=None
):

    insight_generator = InsightGenerator()

    if problem_type == "Regression":
        insight, recommendation = (
            insight_generator.regression_insights_recommendation(
                best_model,
                columns,
                target
            )
        )

    elif problem_type == "Classification":
        insight, recommendation = (
            insight_generator.classification_insights_recommendation(
                best_model,
                columns,
                target
            )
        )

    else:
        insight, recommendation = (
            insight_generator.clustering_insights_recommendation(
                best_model,
                columns
            )
        )

    return insight, recommendation