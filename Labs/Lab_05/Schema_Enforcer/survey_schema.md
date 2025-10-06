| Column Name     | Required Data Type | Brief Description                                       |
| :---            | :---               | :---                                                    |
| `student_id`    | `INT`              | Unique identifier for each student.                     |
| `major`         | `VARCHAR(50)`      | Student’s declared major/department (e.g., "CS").       |
| `GPA`           | `FLOAT`            | Grade point average on a 0.0–4.0 scale.                 |
| `is_cs_major`   | `BOOL`             | True if student is a CS major; otherwise False.         |
| `credits_taken` | `FLOAT`            | Total number of credits completed or in progress.       |