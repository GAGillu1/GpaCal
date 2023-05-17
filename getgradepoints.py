
ref_points = {'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'AB': 3.5, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'BC': 2.5, 'C+': 2.3, 'C': 2.0,
              'C-': 1.7, 'CD': 1.5, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}

# Function to retun the us grade points from the us grade
def get_grade(us_grade):
    for grades, gradepoints in ref_points.items():
        if us_grade == grades:
            return gradepoints