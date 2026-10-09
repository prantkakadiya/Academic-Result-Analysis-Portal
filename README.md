# Academic Result Analysis Portal

A Streamlit-based academic analytics dashboard for viewing, comparing, and analyzing student results across semesters.

## Overview

This project helps faculty, academic coordinators, and administrators analyze student performance from CSV-based academic records. It provides insights into:

- overall class performance
- subject-wise trends
- student-wise analysis
- test comparison over time
- branch-wise and subject-wise rankings

## Features

- Semester selector for multiple academic batches
- Student search by name or enrollment number
- Subject-wise performance statistics
- Test-wise average, highest, lowest, and standard deviation
- Visualizations for marks distribution
- Overall and branch-wise ranking dashboard
- Comparison between a student and class average or another student
- Downloadable student analysis data

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib

## Project Structure

```text
Academic Result Analysis Portal/
├── main/
│   ├── main.py
│   ├── Overview.py
│   ├── Student_Analysis.py
│   ├── Subject_Analysis.py
│   ├── Test_Comparison.py
│   ├── Rankings.py
│   ├── dataLoder.py
│   └── data/
│       ├── sem-1/
│       │   ├── marks.csv
│       │   └── subjects.txt
│       └── sem-2/
│           ├── marks.csv
│           └── subjects.txt
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies:

```bash
pip install streamlit pandas numpy matplotlib
```

## Run the App

From the project folder:

```bash
cd main
streamlit run main.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Data Format

The application reads student academic data from CSV files located in the `main/data` folder. Each semester folder contains:

- `marks.csv` – student marks data
- `subjects.txt` – list of subjects for that semester

## Use Cases

- track academic performance over time
- identify top-performing students
- compare subject strengths and weaknesses
- analyze branch-wise performance
- support faculty decisions with data-driven insights

## License

This project is for educational and academic use.

## Contributor

Developed as a student academic result analysis and reporting dashboard.
