🧠 Smart Resume Parser

An AI-powered desktop app to screen resumes based on job role requirements using Python and NLP.

✨ Key Features

📄 Upload resumes in PDF format

🔍 Extracts name, email, and phone number using spaCy

✅ Matches skills and programming languages with selected job role

📊 Gives a score out of 100 and selection result (Selected / Not Selected)

💾 Saves parsed results and selection summaries to text files

🖥️ Built with a user-friendly Tkinter GUI

🎯 Supported Job Roles

Developer

Data Analyst

Manager

Each role has its own list of required skills and programming languages.

⚙️ How to Use

1. Install dependencies:

pip install pdfplumber spacy rapidfuzz
python -m spacy download en_core_web_sm


2. Run the application:

python main.py


3. Use the GUI to:

Enter your name

Select a role

Upload your PDF resume

View and save results

📁 Output Files

parsed_results.txt – Detailed report of resume analysis

selection_results.txt – Name, role, score, and status (Selected / Not Selected)

🛠 Tech Stack

Python
Tkinter
pdfplumber
spaCy
rapidfuzz

Here's a video reference 📸

https://drive.google.com/file/d/1PIJobeXm7qRKluh8FiUoxIWuRqtrq_b8/view?usp=drivesdk
