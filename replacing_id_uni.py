import pandas as pd

# Load Sheet1 and Sheet2 into separate dataframes
df1 = pd.read_excel(r"grades_data_1.xlsx", sheet_name='Sheet1')
df2 = pd.read_excel(r"grades_data_1.xlsx", sheet_name='Sheet2')

# Create a dictionary mapping university names to their IDs
id_dict = dict(zip(df2['university_name'], df2['uid']))

# Replace university names in Sheet1 with their IDs
df1['University'] = df1['University'].map(id_dict)

# Save the updated Sheet1 dataframe to a new Excel file
df1.to_excel('cal_insertion.xlsx', index=False)
