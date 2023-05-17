#Getting grade points and calculating GPA
from filter_Scale import filtered_scale
from getgradepoints import get_grade
from gpa_log import logger
import pandas as pd

data=[]

''' Caclualating grade points  . 
Input:marks, country, university, credits and course . 
With country and university we will fetch the scale from filtered_scale() function 
Each course marks are converted to usgrade and then its changed to gradepoints using function get_grade()
At the end we are calculating the GPA which is total gradepoints divided by total credits
returning scale,gpa and a table with 'coursename','Credits', 'Marks', 'USGrade', 'GradePoints'
'''
def get_grade_points(marks, country, university,credits,course):
    data.clear()
    df2 = filtered_scale(country, university)
    df2.loc[:,'scales'] = df2['scales'].astype(str)
    logger.debug(df2)

    total_grade_points = 0
    total_credits = 0

    for i in range(0,len(marks)):
        mark = marks[i]

        if len(df2) == 0:
            logger.error('Invalid country or university ',marks)
            return 'Invalid country or university'

        if isinstance(mark, (float, int)):
            # If the input is a scale, get the corresponding US grade
            # us_grade = df2.loc[df2['Scale'] == mark, 'US Grade'].values[0]
            for j in range(len(df2)):
                scale_range = df2['scales'][j].split('-')
                scale_min = float(scale_range[0])
                print(scale_min)
                scale_max = float(scale_range[1]) if len(scale_range) > 1 else float(scale_range[0])
                print(scale_max)
                if mark >= scale_min and mark <= scale_max:
                    us_grade = df2['usgrade'][j]
                    print("------US grade is ", us_grade)

                    break
            else:
                return 'Invalid scale input'
            grade_points = get_grade(us_grade)
        elif mark in df2['grade'].values:
            # If the input is a grade, get the corresponding US grade
            us_grade = df2.loc[df2['grade'] == mark, 'usgrade'].values[0]
            grade_points = get_grade(us_grade)
        else:
            # If the input is neither a scale nor a grade, return an error message
            logger.error('Invalid Scale Input ')
            return 'Invalid input'

        credit = int(credits[i])
        courses=course[i]
        total_grade_points += grade_points * credit
        total_credits += credit
        data.append({'Course': courses, 'Credits': credit, 'Marks': mark,
                                            'USGrade': us_grade, 'GradePoints': grade_points})
        logger.debug(data)


    # Calculate the GPA and return it
    course_table = pd.DataFrame(data,columns=['Course', 'Credits', 'Marks', 'USGrade', 'GradePoints'],index=None)
    gpa = round(total_grade_points / total_credits, 2)
    print(course_table)
    return gpa,course_table,df2