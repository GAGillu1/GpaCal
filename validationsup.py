from flask import Flask, render_template, request, send_file, session, jsonify
import pandas as pd
import os
import datetime
import logging
import psycopg2

####### Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# getiing current working diretor
cwd = os.getcwd()
# defining the app for flask and giving the template folder as current working director and all htmls should be in current working directory
app = Flask(__name__, template_folder=cwd)
# Secret key is for session when we need to push the data from one flask route to another
app.secret_key = 'seccret'

# reading excel whihc has all the data with country names and colleges
#df = pd.read_excel(r'D:\Enr\gradesdup.xlsx', sheet_name='Countries')


# Function to filer the dataframe with given university name and country
def filtered_scale(country, university):
    # df2 = df[(df['Country'] == country) & (df['University'] == university)]
    # logger.debug(df2)
    # return df2.reset_index(drop=True) if not df2.empty else None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="GPA",
            user="postgres",
            password="Ap26ae3726@123"
        )
        cur = conn.cursor()
        query = "SELECT u.university_name, t.grade, t.scales, t.usgrade FROM countries c INNER JOIN universities u ON c.country_id = u.country_id INNER JOIN caltab t ON u.uid = t.university_id WHERE c.country_name =%s AND u.university_name = %s"
        values = (country, university)
        cur.execute(query, values)
        print(cur.query)
        df = pd.read_sql_query(query, conn, params=values)
        print(df)
        return df.reset_index(drop=True) if not df.empty else None
        #
        # engine = create_engine('postgresql://postgres:@localhost:5432/GPA')
        #
        # query = "SELECT c.country_name, u.university_name, t.grade, t.scales, t.usgrade \
        #          FROM countries c \
        #          INNER JOIN universities u ON c.country_id = u.country_id \
        #          INNER JOIN caltab t ON u.uid = t.university_id \
        #          WHERE c.country_name = %s AND u.university_name = %s"
        #
        # params = (country, university)
        #
        # with engine.connect() as conn:
        #     df = pd.read_sql_query(query, con=conn, params=params)
        # print(df)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
        # engine.dispose()


# Ref points for converting the US grade to gradepoints
ref_points = {'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'AB': 3.5, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'BC': 2.5, 'C+': 2.3, 'C': 2.0,
              'C-': 1.7, 'CD': 1.5, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}


# Function to retun the us grade points from the us grade
def get_grade(us_grade):
    for grades, gradepoints in ref_points.items():
        if us_grade == grades:
            return gradepoints


# Data is to append the dataframe since pandas.append is depreciating in future releases(got warning when used)
data = []


# Getting grade points and calculating GPA
def get_grade_points(marks, country, university, credits, course):
    data.clear()
    df2 = filtered_scale(country, university)
    df2.loc[:, 'scales'] = df2['scales'].astype(str)
    logger.debug(df2)

    total_grade_points = 0
    total_credits = 0

    for i in range(0, len(marks)):
        mark = marks[i]

        if len(df2) == 0:
            logger.error('Invalid country or university ', marks)
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
        courses = course[i]
        total_grade_points += grade_points * credit
        total_credits += credit
        data.append({'Course': courses, 'Credits': credit, 'Marks': mark,
                     'US Grade': us_grade, 'Grade Points': grade_points})
        logger.debug(data)

    # Calculate the GPA and return it
    course_table = pd.DataFrame(data, columns=['Course', 'Credits', 'Marks', 'US Grade', 'Grade Points'], index=None)
    gpa = round(total_grade_points / total_credits, 2)

    return gpa, course_table, df2


# Flask routes
@app.route('/')
def index():
    return render_template(r'index101.html')


@app.route('/calculate_gpa', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print('hai')
        session.pop('df', None)

        data = request.get_json()
        if not data:
            return "Json Empty"
        elif 'country' not in data or not data['country'] and len(data['country'])>15:
            return "country is empty or country contains more than 20 values "
        elif 'grades' not in data or not data['grades'] :
            print("No data")
            return "Grade is empty"


        elif 'credits' not in data or not data['credits'] :
            return "Credits are empty"
        else:
            print(data)


            country = data['country']
            logger.info(f"Received POST request with country={country}")

            course = data['courses']
            course = list(filter(None, course))
            logger.info(f"Received POST request with course={course}")

            credits = data['credits']
            credits = list(filter(None, credits))
            logger.info(f"Received POST request with credits={credits}")

            marks = data['grades']
            marks_unf = list(filter(None, marks))
            marks = [float(x) if '.' in x else int(x) if x.isdigit() else x for x in marks_unf]
            logger.info(f"Received POST request with marks={marks}")

            university = 'Avinashilingam Institute for Home Science and Higher Education for Women'
            print(credits)
            # Calculate the GPA and render the template with it

            gpa, output, scale = get_grade_points(marks, country, university, credits, course)
            out_html = output.to_html()
            scale_html = scale.to_html()
            session['df'] = output.to_dict('records')
            logger.info(f"Calculated GPA={gpa}")
            print(output)
            if isinstance(gpa, str):
                return jsonify({'error': gpa})

            # return render_template(r'index_1.html',output=out_html,gpa=gpa,scale=scale_html)
            return jsonify({'gpa': gpa, 'course_table': output.to_dict('records'), 'scale': scale.to_dict('records')})

            # Render the home template for a GET request
        logger.info("Received GET request")

        return render_template(r'index_101.html')

    @app.route('/download_excel')
    def download_excel():
        output = pd.DataFrame.from_dict(session['df'])
        time = datetime.datetime.now()
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
        with pd.ExcelWriter('data.xlsx') as writer:
            output.to_excel(writer, index=False)

        # Send the Excel file as a download
        # download="output"+".xlsx"
        logger.info("Excel file downloaded")

        return send_file("data.xlsx", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)


