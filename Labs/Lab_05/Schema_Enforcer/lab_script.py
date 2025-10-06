import csv
import json
import pandas as pd

# task 1
data = [
    ["student_id", "major", "GPA", "is_cs_major", "credits_taken"],
    [1, "CS", 3.5, 'Yes', '12.0'],
    [2, "APMA", 3, 'No', '15.5'],
    [3, "EE", 2.8, 'No', '13'],
    [4, "ME", 3.2, 'No', '20'],
    [5, "CS", 2.8, 'Yes', '28']
]

# write this data into csv 'raw_survey_data.csv'
with open("raw_survey_data.csv", "w", newline="") as file_pointer:
    writer = csv.writer(file_pointer)
    writer.writerows(data)

# task 2
courses = [
  {
    "course_id": "DS2002",
    "section": "001",
    "title": "Data Science Systems",
    "level": 200,
    "instructors": [
      {"name": "Austin Rivera", "role": "Primary"}, 
      {"name": "Heywood Williams-Tracy", "role": "TA"} 
    ]
  },
  {
    "course_id": "CS4991",
    "section": "001",
    "title": "Capstone Technical Report",
    "level": 400,
    "instructors": [
      {"name": "Rosanne Vrugtman", "role": "Primary"},
      {"name": "Briana Morrison", "role": "Technical Advisor"},
      {"name": "Maggie Nunley", "role": "Science and Engineering Research Librarian"}
    ]
  },
  {
    "course_id": "STS4600",
    "section": "001",
    "title": "The Engineer, Ethics, and Professional Responsibility",
    "level": 400,
    "instructors": [
      {"name": "Peter Norton", "role": "Primary"}
    ]
  }
]

# raw_course_catalog.json
with open("raw_course_catalog.json", "w") as fp:
    json.dump(courses, fp, indent=2)

# task 3
df = pd.read_csv("raw_survey_data.csv")

# enforce boolean conversion for is_cs_major
df["is_cs_major"] = (
    df["is_cs_major"].astype(str).str.strip().str.lower().map({"yes": True, "no": False})
)

# enforce float types for GPA and credits_taken
df = df.astype({
    "GPA": "float64",
    "credits_taken": "float64"
})

# write cleaned data
df.to_csv("clean_survey_data.csv", index=False)

# task 4
with open("raw_course_catalog.json", "r") as fp:
    data = json.load(fp)

# flatten hierarchical JSON
df_norm = pd.json_normalize(
    data,
    record_path=["instructors"],
    meta=["course_id", "title", "level", "section"],
    errors="ignore"  # safe for missing section keys
)

# write normalized course catalog
df_norm.to_csv("clean_course_catalog.csv", index=False)
