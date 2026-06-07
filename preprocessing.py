import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

class DataPreprocessor:
    test_size=0.2
    random_state=42

    def preprocess(self,file_path,problem_type):
        df = pd.read_csv(file_path)
        df = self.remove_Id_Columns(df)
        df = self.handle_missing_values(df)
        target_column=df.columns[-1]
        if problem_type in ["Regression", "Classification"]:
            X,y =self.split_features_target(df,target_column)
            X_train,X_test,y_train,y_test=self.split_train_test(X,y)
            X_train,X_test=self.encode_features(X_train,X_test)
            if problem_type=="Classification":
                y_train,y_test=self.encode_target(y_train,y_test)
            X_train,X_test=self.scaling_features(X_train,X_test)
            return X_train,X_test,y_train,y_test
        elif problem_type=="Clustering":
            X_train,X_test=train_test_split(df,test_size=self.test_size,random_state=self.random_state)
            X_train,X_test=self.encode_features(X_train,X_test)
            X_train,X_test=self.scaling_features(X_train,X_test)
            return X_train,X_test
        else:
            return 'Invalid problem type.'
    
    def remove_Id_Columns(self,df):
        for col in df.columns:
            if (col == "id" or col.endswith("_id")or df[col].nunique() == len(df)):
               df=df.drop(col,axis=1)
        return df

    def handle_missing_values(self,df):
        for column in df.columns:
          if pd.api.types.is_numeric_dtype(df[column]):
            df[column]=df[column].fillna(df[column].mean())
          else:
            df[column]=df[column].fillna(df[column].mode()[0])
        return df
     
    def encode_features(self,X_train,X_test):
        labelEncoder=LabelEncoder()
        for column in X_train.columns:
            if not pd.api.types.is_numeric_dtype(X_train[column]):
                unique_values=X_train[column].unique()
                if(len(unique_values)==2):
                    X_train[column]=labelEncoder.fit_transform(X_train[column])
                    X_test[column]=labelEncoder.transform(X_test[column])
                else:
                    X_train=pd.get_dummies(X_train,columns=[column],drop_first=True)
                    X_test=pd.get_dummies(X_test,columns=[column],drop_first=True)
        return X_train, X_test
    
    def encode_target(self, y_train, y_test):
       labelEncoder = LabelEncoder()
       y_train = labelEncoder.fit_transform(y_train)
       y_test = labelEncoder.transform(y_test)
       return y_train, y_test
    
    def scaling_features(self,X_train,X_test):
        scaler=StandardScaler()
        numerical_col=X_train.select_dtypes(include=['int64','float64']).columns
        X_train[numerical_col]=pd.DataFrame(scaler.fit_transform(X_train[numerical_col]), columns=numerical_col,index=X_train.index)
        X_test[numerical_col]=pd.DataFrame(scaler.transform(X_test[numerical_col]), columns=numerical_col,index=X_test.index)
        return X_train, X_test
    
    def split_features_target(self,df,target_column):
        X=df.drop(target_column,axis=1)
        y=df[target_column]
        return X, y
    
    def split_train_test(self,X,y):
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=self.test_size,random_state=self.random_state)
        return X_train,X_test,y_train,y_test

   
