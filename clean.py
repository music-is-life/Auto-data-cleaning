# importing libaries:
import sys
import pandas as pd
import numpy as np
import re
# cleaning the data function:
def DataCleaner():

    # import df
    csv_name = sys.argv[1]
    dataset = pd.read_csv(csv_name)
    
    ###data Exploration:
    
    #removing lines and columns that all nulls.
    df = dataset.dropna(axis = 0, how = 'all')
    df = df.dropna(axis = 1, how = 'all')
    
    #removing columns that has less then 25% data of the lines size:
    df = df.dropna(axis = 1, thresh = int(dataset.shape[0] * 0.25))
    
    #removing duplicates (columns, rows):
    df.drop_duplicates(inplace = True) # rows
    df = df.loc[:,~df.T.duplicated()] # columns (based on columns titles)
    
    #inplace Nan values:
    from sklearn.impute import SimpleImputer
    float_df = df.loc[:,df.dtypes=='float64'].shape[1]
    int_df = df.loc[:,df.dtypes=='int64'].shape[1]
    object_df = df.loc[:,df.dtypes=='object'].shape[1]
    
    
    #inplace Nan values for objects.
    imputer = SimpleImputer(missing_values = np.nan, strategy = 'most_frequent')
    if (object_df > 0):
        imputer = imputer.fit(df.loc[:,df.dtypes=='object'])
        df.loc[:,df.dtypes=='object'] = imputer.transform(df.loc[:,df.dtypes=='object'])
    
    
    #inplace Nan values for numeric mean of the columns:
    imputer = SimpleImputer(missing_values = np.nan, strategy = 'mean')
    if (int_df > 0):
        imputer = imputer.fit(df.loc[:,df.dtypes=='int64'])
        df.loc[:,df.dtypes=='int64'] = imputer.transform(df.loc[:,df.dtypes=='int64'])
    if (float_df > 0):
        imputer = imputer.fit(df.loc[:,df.dtypes=='float64'])
        df.loc[:,df.dtypes=='float64'] = imputer.transform(df.loc[:,df.dtypes=='float64'])
    
    # remove same values in all column (it dosnt change the weight):
    isRepeat = []
    for i in df:
        if ((df[i][2] == df[i]).all()):
            isRepeat.append(i)
    df.drop(columns = isRepeat, inplace = True)
    
    ### Standirization:
        
    # fix misstype errors such as(.,`) and capitilzation in objects column:
    for i in df:
        if(df[i].dtype == 'object'):
            df[i] = df[i].apply(lambda x: re.sub('[`.]', '', x ).capitalize())
    
    ### Normalization:
        
    #seperate columns by that has "," in the data:
    names = []
    for i in df:
        if(df[i].dtype == 'object'):
            z = df[i].str.split(",",n=2, expand=True)
            if (z.columns.size > 1):
                for j in range(z.columns.size):
                    names.append(f"{i}{j+1}")
                df[names] = z.values
                names = []
        else: 
            continue
        if (z.columns.size > 1):
            df.drop(columns=i, inplace=True)
            
    ### Exporting Csv file:
    new_csv_name = csv_name.replace('.csv','')
    df.to_csv(f"{new_csv_name}_cleaned.csv")
    
DataCleaner()





