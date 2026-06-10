import pandas as pd

class DatasetAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
    def get_rows(self):
        return self.data.shape[0]
    def get_columns(self):
        return self.data.shape[1]
    def get_column_names(self):
        return self.data.columns.tolist()
    def get_missing_values(self):
        return self.data.isnull().sum().to_dict()
    def get_data_types(self):
        return self.data.dtypes.to_dict()
    def get_summary(self):
        summary = {
            'num_rows': self.get_rows(),
            'num_columns': self.get_columns(),
            'column_names': self.get_column_names(),
            'missing_values': self.get_missing_values(),
            'data_types': self.get_data_types()
        }
        return summary
class ProblemDetector:
    def __init__(self):
        self.problems = {
            1: "Regression",
            2: "Classification",
            3: "Clustering",
            4: "Time Series Forecasting"
        }