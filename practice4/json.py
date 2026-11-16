# Practice 04 - JSON Parsing and Creation

import json
from pathlib import Path

# 1. JSON string
json_string = """
{
    "name": "Anzor",
    "age": 18,
    "student": true,
    "skills": ["Python", "C++", "HTML"]
}
"""

# 2. Parse JSON with json.loads()
data = json.loads(json_string)

print("Parsed JSON:")
print(data)
print("Name:", data["name"])
print("Age:", data["age"])
print("Skills:", data["skills"])

# 3. Convert Python to JSON with json.dumps()
student = {
    "name": "Anzor",
    "age": 18,
    "university": "KBTU",
    "subjects": ["Python", "Math", "Programming"],
    "active": True
}

json_output = json.dumps(student, indent=4)

print("\nPython dictionary converted to JSON:")
print(json_output)

# 4. Write JSON to a file
output_file = Path("student.json")
with output_file.open("w", encoding="utf-8") as file:
    json.dump(student, file, indent=4)

print("\nJSON file created:", output_file)

# 5. Read JSON from a file
with output_file.open("r", encoding="utf-8") as file:
    loaded_student = json.load(file)

print("\nData read from student.json:")
print(loaded_student)

# 6. Read sample-data.json if it is available
sample_file = Path("sample-data.json")

if sample_file.exists():
    with sample_file.open("r", encoding="utf-8") as file:
        sample_data = json.load(file)

    print("\nData from sample-data.json:")
    print(json.dumps(sample_data, indent=4))
else:
    print("\nsample-data.json was not found.")
    print("Place the teacher's sample-data.json next to this file.")

# 7. JSON-compatible Python data types
example = {
    "string": "Hello",
    "number": 42,
    "decimal": 3.14,
    "boolean": True,
    "none": None,
    "list": [1, 2, 3],
    "object": {"city": "Almaty"}
}

print("\nJSON-compatible Python object:")
print(json.dumps(example, indent=4))
