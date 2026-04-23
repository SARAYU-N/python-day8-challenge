import random
import math
import numpy as np
import pandas as pd

roll_last_digit = 8
num_students = 10

def generate_data(n):
    records = []
    for i in range(1, n + 1):
        student_id = "STU" + str(i)
        marks = random.randint(0, 100)
        attendance = random.randint(0, 100)
        assignment = random.randint(0, 50)
        records.append((student_id, marks, attendance, assignment))
    return records

def classify_students(df):
    categories = {}
    for i in range(len(df)):
        sid = df.loc[i, "student_id"]
        marks = df.loc[i, "marks"]
        attendance = df.loc[i, "attendance"]

        if marks < 40 or attendance < 50:
            categories[sid] = "At Risk"
        elif marks > 90 and attendance > 80:
            categories[sid] = "Top Performer"
        elif marks >= 71 and marks <= 90:
            categories[sid] = "Good"
        else:
            categories[sid] = "Average"
    return categories

def analyze_data(df):
    marks = df["marks"].to_numpy()
    attendance = df["attendance"].to_numpy()

    mean_marks = np.mean(marks)
    median_marks = np.median(marks)
    std_marks = np.std(marks)
    correlation = np.corrcoef(marks, attendance)[0][1]

    min_marks = np.min(marks)
    max_marks = np.max(marks)

    normalized = []
    for x in marks:
        value = (x - min_marks) / (max_marks - min_marks)
        normalized.append(round(value, 2))

    df["normalized_marks"] = normalized

    return mean_marks, median_marks, std_marks, correlation

def final_insight(df, categories, std_marks):
    low_attendance = len(df[df["attendance"] < 50])
    top_count = list(categories.values()).count("Top Performer")

    if std_marks < 15 and top_count >= 2 and low_attendance <= 3:
        return "Stable Academic System"
    elif low_attendance > 3:
        return "Critical Attention Required"
    else:
        return "Moderate Performance"

records = generate_data(num_students)

df = pd.DataFrame(records, columns=[
    "student_id", "marks", "attendance", "assignment"
])

unique_attendance = set(df["attendance"])

df["performance_index"] = [
    round((m * 0.6 + a * 0.4) * math.log(att + 1), 2)
    for m, a, att in zip(df["marks"], df["assignment"], df["attendance"])
]

categories = classify_students(df)

mean_marks, median_marks, std_marks, correlation = analyze_data(df)

summary = (round(mean_marks, 2), round(std_marks, 2), int(np.max(df["marks"])))

insight = final_insight(df, categories, std_marks)

print("===== DATAFRAME =====")
print(df)

print("\n===== CATEGORY DICTIONARY =====")
print(categories)

print("\n===== STATISTICS =====")
print("Mean Marks:", round(mean_marks, 2))
print("Median Marks:", round(median_marks, 2))
print("Std Deviation:", round(std_marks, 2))
print("Correlation:", round(correlation, 2))

print("\nTuple Output:")
print(summary)

print("\nUnique Attendance Values:", unique_attendance)

print("\n===== FINAL INSIGHT =====")
print(insight)

