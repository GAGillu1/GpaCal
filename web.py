import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.scholaro.com/db/Countries/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
ul_element = soup.find("ol", {'id': 'countriesList'})
li_elements = ul_element.find_all("li")
countries=[li.text.strip() for li in li_elements]

dfs=[]
for country in countries:
    for page in range(0,6):
        base_url = f"https://www.scholaro.com/db/Countries/{country}/Grading-System/page/{page}"
        print("\n")
        print("Scraping data from:", country)

        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.findAll("div", {'class': 'col-md-6 mb-4'})
        if table:

         for tab in table:
            college = tab.find("h2").text
            header = tab.find_all("th")
            header_row = [th.text.strip() for th in header]

            data_rows = tab.find_all("tr")
            table_data = []
            for row in data_rows:
                cells = row.find_all("td")
                row_data = [cell.text.strip() for cell in cells]
                table_data.append(row_data)

            df = pd.DataFrame(table_data, columns=header_row)

            df["Country"] = country  # Add country column
            df["University"] = college  # Add university column

            if "Grade" in df.columns:
                if "Scale" in df.columns:
                    df = df[['Country', 'University', 'Grade', 'Scale', 'US Grade']]
                else:
                    df = df[['Country', 'University', 'Grade', 'US Grade']]
            elif "Scale" in df.columns:
                df = df[['Country', 'University', 'Scale', 'US Grade']]
            else:
                df = df[['Country', 'University', 'US Grade']]

                pass

            dfs.append(df)

df1 = pd.concat(dfs)
print(df1)
df1.to_excel('grades_data_1.xlsx', index=False)


