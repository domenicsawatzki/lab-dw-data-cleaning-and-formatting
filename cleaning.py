import pandas as pd

def cleaningGender(x):
    if x in ['M', 'MALE']:
        return 'Male'
    elif x.startswith('F'):
        return 'Female'
    else:
        return x
        
def cleaningState(x):
    if x in ['WA']:
        return 'Washington'
    elif x in ['Cali']:
        return 'California'
    elif x in ['AZ']:
        return 'Arizona'
    else: 
        return x
    
def columnCleaning(dataframe):
    dataframe.columns= [col.lower() for col in dataframe.columns]
    dataframe.columns= [col.replace(' ', '_') for col in dataframe.columns]
    dataframe.rename(columns={'st':'state'}, inplace=True)
    dataframe.rename(columns={'monthly_premium_auto':'monthly_premium_costs'}, inplace=True)
    
    return dataframe 
    
def cleaningValues(dataframe):
   

    # CLEANING NULL VALUES
    dataframe = dataframe.dropna(subset=['customer'])
    
    # Exercise 4: fill the missing gender values -> destribution between men and female was not so far away from each other and using all null values with only one type of them (men | female ) had a big impact of distribution 
   
    # checking code
    # print(df['gender'].unique())
    # genderCounts = df['gender'].value_counts(dropna=False)
    # print(genderCounts) 
    # CLEANING GENDER COLUMN
    dataframe['gender'] = dataframe['gender'].fillna(method='bfill')
    # dataframe['gender'] = list(map(str.upper, dataframe['gender']))
    # dataframe['gender'] = list(map(cleaningGender, dataframe['gender']))
    dataframe['gender'] = dataframe['gender'].str.upper()
    dataframe['gender'] = dataframe['gender'].map(cleaningGender)


    
    #checking code
    # print(df['gender'].unique())
    # print(genderCounts)

 
    # CLEANING STATE COLUMN
    dataframe['state'] = list(map(cleaningState, dataframe['state']))
   
    
    # CLEAINING EDUCATION COLUMN
    dataframe['education'] = dataframe['education'].str.replace('Bachelors', 'Bachelor')
    dataframe['education'].unique()
    
    # CLEANING CUSTOMER LIFETIME VALUE COLUMN
    # Using median to fill null values
    dataframe['customer_lifetime_value'] = dataframe['customer_lifetime_value'].str.replace('%', '')
    dataframe['customer_lifetime_value'] =  pd.to_numeric(dataframe['customer_lifetime_value'], errors='coerce')

    customer_lifetime_median = dataframe['customer_lifetime_value'].median()
    dataframe['customer_lifetime_value'] = dataframe['customer_lifetime_value'].fillna(customer_lifetime_median)
    
    # SPLITING NUMBER OF OPEN COMPLAINTS COLUMN
    # Assuming that the 3 different values [x/x/xx] representing different status of tickets or something like this e.g. [number of closed tickets/number of tickets in progress/open tickets] or different types of complaints 
    dataframe[['complaint_type1', 'complaint_type2', 'complaint_type3']] = dataframe['number_of_open_complaints'].str.split('/', expand=True)

    dataframe['complaint_type1'] =  pd.to_numeric(dataframe['complaint_type1'], errors='coerce')
    dataframe['complaint_type2'] =  pd.to_numeric(dataframe['complaint_type2'], errors='coerce')
    dataframe['complaint_type3'] =  pd.to_numeric(dataframe['complaint_type3'], errors='coerce')
    
    # CLEANING INCOME COLUMN
    
    income_median= dataframe['income'].median()
    dataframe['income'] = dataframe['income'].replace(0, income_median)

    dataframe['income'].value_counts()
    
    return dataframe
    
    
def clean(dataframe):
    dataframe = columnCleaning(dataframe)
    dataframe
    dataframe = cleaningValues(dataframe)
    
    return dataframe
        
        
