import pandas as pd


df = pd.read_excel(r'D:\Enr\gradesdup.xlsx', sheet_name='Countries')
marksunf=['9.3','K']
marks = [float(x) if '.' in x else int(x) if x.isdigit() else x for x in marksunf]
#marks = [float(x) if isinstance(x, str) and '.' in x else x for x in marksunf]

for i in range(len(marks)):
    print((marks[i]))
country='India'
university='Avinashilingam Institute for Home Science and Higher Education for Women'

def filtered_scale(country, university):
    df2 = df[(df['Country'] == country) & (df['University'] == university)]
    return df2.reset_index(drop=True) if not df2.empty else None



ref_points = {'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'AB': 3.5, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'BC': 2.5, 'C+': 2.3, 'C': 2.0,
              'C-': 1.7, 'CD': 1.5, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}


def get_grade(us_grade):
    for grades, gradepoints in ref_points.items():
        if us_grade == grades:
            return gradepoints
data=[]    # createated as we got warning for pandas.append which will be removed from future versions

def get_grade_points(marks, country, university,credits,course):
    df2 = filtered_scale(country, university)
    df2.loc[:, 'Scale'] = df2['Scale'].astype(str)

    total_grade_points = 0
    total_credits = 0

    for i in range(0,len(marks)):
        mark = marks[i]

        if len(df2) == 0:
            return 'Invalid country or university'



        # Check if the input is a grade or a scale
        if isinstance(mark, (float, int)):
            # If the input is a scale, get the corresponding US grade
            #us_grade = df2.loc[df2['Scale'] == mark, 'US Grade'].values[0]
            for j in range(len(df2)):
                scale_range = df2['Scale'][j].split('-')
                scale_min = float(scale_range[0])
                print(scale_min)
                scale_max = float(scale_range[1]) if len(scale_range) > 1 else float(scale_range[0])
                print(scale_max)
                if mark >= scale_min and mark <= scale_max:
                    us_grade = df2['US Grade'][j]
                    print("------US grade is ",us_grade)

                    break
            else:
                return 'Invalid scale input'
            grade_points = get_grade(us_grade)
        elif mark in df2['Grade'].values:
            # If the input is a grade, get the corresponding US grade
            us_grade = df2.loc[df2['Grade'] == mark, 'US Grade'].values[0]
            grade_points = get_grade(us_grade)
        else:
            # If the input is neither a scale nor a grade, return an error message
            return 'Invalid input'

        credit = int(credits[i])
        courses=course[i]
        total_grade_points += grade_points * credit
        total_credits += credit
        data.append({'Course': courses, 'Credits': credit, 'Marks': mark,
                                            'US Grade': us_grade, 'Grade Points': grade_points})


    # Calculate the GPA and return it
    course_table = pd.DataFrame(data,columns=['Course', 'Credits', 'Marks', 'US Grade', 'Grade Points'],index=None)
    gpa = round(total_grade_points / total_credits, 2)
    print(course_table)
    return gpa,course_table,df2




course=["abc","def"]
credits=[3,3]
g=get_grade_points(marks, country, university,credits,course)
print("G is******",g)