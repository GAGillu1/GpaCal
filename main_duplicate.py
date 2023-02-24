from flask import Flask, render_template, request,send_file,session
import pandas as pd
import os
import datetime





cwd = os.getcwd()

app = Flask(__name__, template_folder=cwd)
app.secret_key = 'seccret'


# Load the data from the Excel sheet into a Pandas DataFrame
df = pd.read_excel(r'D:\Enr\grades.xlsx', sheet_name='Countries')


def filtered_scale(country, university):
    df2 = df[(df['Country'] == country) & (df['University'] == university)]
    return df2



ref_points = {'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'AB': 3.5, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'BC': 2.5, 'C+': 2.3, 'C': 2.0,
              'C-': 1.7, 'CD': 1.5, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}


def get_grade(us_grade):
    for grades, gradepoints in ref_points.items():
        if us_grade == grades:
            return gradepoints

extdf=[]
def get_grade_points(marks, country, university,credits,course):
    df2 = filtered_scale(country, university)
    df2['Scale'] = df2['Scale'].astype(str)
    course_table = pd.DataFrame(columns=['Course', 'Credits', 'Marks', 'US Grade', 'Grade Points'])
    print("df2scale",df2['Scale'])

    total_grade_points = 0
    total_credits = 0

    for i in range(0,len(marks)):
        mark = marks[i]

        if len(df2) == 0:
            return 'Invalid country or university'

        print(df2)
        print("df2*******", type(df2['Scale'][i]))
        # Check if the input is a grade or a scale
        if mark in df2['Scale'].values:
            # If the input is a scale, get the corresponding US grade
            us_grade = df2.loc[df2['Scale'] == mark, 'US Grade'].values[0]
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
        course_table = course_table.append({'Course': courses, 'Credits': credit, 'Marks': mark,
                                            'US Grade': us_grade, 'Grade Points': grade_points}, ignore_index=True)


    # Calculate the GPA and return it

    gpa = round(total_grade_points / total_credits, 2)
    print(course_table)
    return gpa,course_table,df2


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        country = request.form['country']
        course = request.form.getlist('course')
        course=list(filter(None, course))
        credits = request.form.getlist('credits')
        credits=list(filter(None, credits))
        marks = request.form.getlist('grade')
        marks=list(filter(None,marks))
        university = 'Aligarh Muslim University'
        print(credits)

        # Calculate the GPA and render the template with it
        gpa,output,scale = get_grade_points(marks, country, university,credits,course)
        out_html=output.to_html()
        scale_html=scale.to_html()
        session['df']=output.to_dict('records')
        #out_html="abc"
        print(out_html)
        return render_template(r'home.html',output=out_html,gpa=gpa,scale=scale_html)



    # Render the home template for a GET request
    return render_template(r'home.html')


@app.route('/download_excel')
def download_excel():
    output=pd.DataFrame.from_dict(session['df'])
    time = datetime.datetime.now()
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    with pd.ExcelWriter('data.xlsx') as writer:
        output.to_excel(writer, index=False)

    # Send the Excel file as a download
    #download="output"+".xlsx"
    return send_file("data.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


