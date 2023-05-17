import pandas as pd


df = pd.read_excel(r'D:\Enr\grades.xlsx', sheet_name='Countries')
marks='10'
country='India'
university='Aligarh Muslim University'
for i in range(0, len(df)):
    df2 = df[(df['Country'] == 'India') & (df['University'] == 'Aligarh Muslim University')]
if int(marks) in df2['Scale'].values:
    print('Hai')



def filtered_scale(country,university):
    for i in range(0,len(df)):
        df2 = df[(df['Country'] == country) & (df['University'] == university)]
        return df2

def get_grade_points(marks,country,university):
        df2=filtered_scale(country,university)
        df2['Scale']=df2['Scale'].astype(str)
        print(type(df2['Scale']))

        for i in range(0,len(df2)):
            if len(df2) == 0:
                return 'Invalid country'
                # Check if the input is a grade or a scale
            if marks in df2['Scale'].values:
                # If the input is a scale, get the corresponding US grade
                us_grade = df2.loc[df2['Scale'] == marks, 'US Grade'].values[0]
                grade_points=get_grade(us_grade)
            elif marks in df2['Grade'].values:
                # If the input is a grade, get the corresponding US grade
                us_grade = df2.loc[df2['Grade'] == marks, 'US Grade'].values[0]
                grade_points = get_grade(us_grade)
            else:
                # If the input is neither a scale nor a grade, return an error message
                return 'Invalid input'
            return grade_points

ref_points = {'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'AB': 3.5, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'BC': 2.5, 'C+': 2.3, 'C': 2.0,
              'C-': 1.7, 'CD': 1.5, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}
def get_grade(us_grade):
    for grades, gradepoints in ref_points.items():
        if us_grade == grades:
            return gradepoints








print(get_grade_points(marks,country,university))




