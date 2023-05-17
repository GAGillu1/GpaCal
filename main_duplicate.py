import openpyxl
from flask import Flask, render_template, request,send_file,session,jsonify
import pandas as pd
import os
import datetime
import psycopg2
import sqlalchemy
import gpa_log
from openpyxl import load_workbook

from countries import  countries_list
from filter_Scale import filtered_scale
from gradepoints import get_grade_points
from slatelog import slate_log
from universities import universityList

# getting current working diretory
cwd = os.getcwd()
app = Flask(__name__, template_folder=cwd)
# Secret key is for session when we need to push the data from one flask route to another
app.secret_key = 'seccret'


# Flask routes
@app.route('/')
def index():
    return render_template(r'index101.html',)
@app.route('/country',methods=['GET','POST'])
#route for displaying countries
def defa():
    if request.method=='GET':
        countr=countries_list()
        return jsonify({'countries':countr.to_dict('records')})
# route for displaying universities
@app.route("/university",methods=['GET','POST'])
def uni():
    if request.method=='POST':
        data=request.get_json()
        country=data
        uni=universityList(country)
        return jsonify({'university':uni.to_dict('records')})
#route for displaying gradesTable
@app.route("/gradesTable",methods=['GET','POST'])
def optcount():
    if request.method=='POST':
        data=request.get_json()
        country=data['country']
        university=data['university']
        scales=filtered_scale(country,university)
        return jsonify({'course_table': scales.to_dict('records')})

# route for displaying GPA
@app.route('/calculate_gpa', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session.pop('df', None)

        data=request.get_json()
        country = data['country']
        gpa_log.logger.info(f"Received POST request with country={country}")
        course =data['courses']
        #course=list(filter(None, course))
        course = ["" if c is None else c for c in data['courses']]
        gpa_log.logger.info(f"Received POST request with course={course}")
        credits = data['credits']
        credits = list(filter(None, credits))
        gpa_log.logger.info(f"Received POST request with credits={credits}")
        marks = data['grades']
        marks_unf=list(filter(None,marks))
        marks = [float(x) if '.' in x else int(x) if x.isdigit() else x for x in marks_unf]
        gpa_log.logger.info(f"Received POST request with marks={marks}")

        # Calculate the GPA and render the template with it
        university=data['gScale']
        slateId=data['slateId']
        if not slateId:
            slateId=""

        gpa,output,scale = get_grade_points(marks, country, university,credits,course)
        session['df']=output.to_dict('records')
        gpa_log.logger.info(f"Calculated GPA={gpa}")


        df_existing = pd.read_excel('slate.xlsx')
        dict={'SlateID':[slateId],'University/Scale Used':[university],'GPA':[gpa]}
        slateframe=pd.DataFrame(dict)
        df_combined = pd.concat([df_existing, slateframe], ignore_index=True)
        df_combined.to_excel('slate.xlsx', index=False)
        try:
            print(slateId,university,gpa)
            slate_log(slateId,university,gpa)
        except Exception as e:
            print(e)

        if isinstance(gpa, str):
            return jsonify({'error': gpa})

        #return render_template(r'index_1.html',output=out_html,gpa=gpa,scale=scale_html)
        return jsonify({'gpa': gpa, 'course_table': output.to_dict('records'), 'scale': scale.to_dict('records')})




    # Render the home template for a GET request
    gpa_log.logger.info("Received GET request")

    return render_template(r'index_101.html')

# route for downloading excel when download button is hit
@app.route('/download_excel')
def download_excel():
    output=pd.DataFrame.from_dict(session['df'])
    time = datetime.datetime.now()
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    with pd.ExcelWriter('data.xlsx') as writer:
        output.to_excel(writer, index=False)


    # Send the Excel file as a download
    #download="output"+".xlsx"
    gpa_log.logger.info("Excel file downloaded")

    return send_file("data.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


