import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pdfplumber
import spacy
import re
import os
from rapidfuzz import fuzz

nlp = spacy.load("en_core_web_sm")

# --- Role criteria ---
role_criteria = {
    "Developer": {
        "skills": ["web development", "problem solving", "html", "css", "communication"],
        "languages": ["python", "java", "javascript"]
    },
    "Data Analyst": {
        "skills": ["data analysis", "machine learning", "excel", "visualization"],
        "languages": ["python", "r", "sql"]
    },
    "Manager": {
        "skills": ["leadership", "project management", "communication"],
        "languages": ["python", "excel"]
    }
}

# --- Extraction Functions ---
def extract_text_lines(file_path):
    lines = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines += [line.strip() for line in text.split("\n") if line.strip()]
    return lines

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not found"

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9_.+-]+@gmail\.com", text)
    return match.group(0) if match else "Not found"

def extract_phone(text):
    match = re.search(r"\b(?:\+?\d{1,3}[\s\-]?)?(?:\(?\d{2,4}\)?[\s\-]?)?\d{6,10}\b", text)
    return match.group(0) if match else "Not found"

def extract_skills(text):
    return text.lower()

def extract_languages(text):
    return text.lower()

def fuzzy_match(required, actual_text):
    matches = []
    for item in required:
        if any(fuzz.partial_ratio(item, line) > 80 for line in actual_text.split(',')):
            matches.append(item)
    return matches

def reset_form():
    name_entry.delete(0, tk.END)
    role_var.set("")
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)
    loading_label.config(text="")

def clear_form():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear the form?"):
        reset_form()
        messagebox.showinfo("Signed Out", "Form has been cleared.")

def save_to_text_file(data_string):
    with open("parsed_results.txt", "a", encoding="utf-8") as f:
        f.write(data_string + "\n\n")

# --- NEW: Save selection result to second file based on cutoff ---
def save_selection_result(name, role, score):
    status = "Selected" if score >= 75 else "Not Selected"
    with open("selection_results.txt", "a", encoding="utf-8") as f:
        f.write(f"Name: {name}\nRole: {role}\nScore: {score}/100\nStatus: {status}\n{'-'*40}\n")

def process_resume():
    name = name_entry.get().strip()
    role = role_var.get()

    if not name:
        messagebox.showwarning("Input Error", "Please enter your name.")
        return
    if role not in role_criteria:
        messagebox.showwarning("Input Error", "Please select a job role.")
        return

    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    try:
        loading_label.config(text="Processing resume...")
        root.update()

        lines = extract_text_lines(file_path)
        full_text = "\n".join(lines)

        extracted_name = extract_name(full_text)
        email = extract_email(full_text)
        phone = extract_phone(full_text)
        skill_text = extract_skills(full_text)
        lang_text = extract_languages(full_text)

        required = role_criteria[role]
        matched_skills = fuzzy_match(required["skills"], skill_text)
        matched_langs = fuzzy_match(required["languages"], lang_text)

        skill_score = int((len(matched_skills) / len(required["skills"])) * 50)
        lang_score = int((len(matched_langs) / len(required["languages"])) * 50)
        total_score = skill_score + lang_score

        result = f"""
============================== RESUME PARSE REPORT ==============================

Applicant Name     : {name}
Parsed Name        : {extracted_name}
Email              : {email}
Phone              : {phone}
Job Role Applied   : {role}

------------------------------ MATCHING SUMMARY -------------------------------

Matched Skills     : {', '.join(matched_skills) or 'None'}
Matched Languages  : {', '.join(matched_langs) or 'None'}

------------------------------- FILE INFO -------------------------------------

Resume File        : {os.path.basename(file_path)}

===============================================================================
"""

        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
        result_text.config(state=tk.DISABLED)

        save_to_text_file(result)
        save_selection_result(name, role, total_score)  # <-- NEW save selection result

        messagebox.showinfo("Success", f"Resume processed. Score: {total_score}/100")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process resume:\n{e}")

    finally:
        loading_label.config(text="")

# --- GUI Setup ---
root = tk.Tk()
root.title("Smart Resume Parser")
root.geometry("650x700")
root.configure(bg="#f4f4f4")

style = ttk.Style()
style.configure("TButton", font=("Arial", 11), padding=5)
style.configure("TLabel", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

ttk.Label(frame, text="AI Resume Screening Portal", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

ttk.Label(frame, text="Enter Your Name:").grid(row=1, column=0, sticky="e", pady=5)
name_entry = ttk.Entry(frame, width=30)
name_entry.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Select Job Role:").grid(row=2, column=0, sticky="ne", pady=5)
role_var = tk.StringVar()
roles_frame = ttk.Frame(frame)
roles_frame.grid(row=2, column=1, sticky="w")
for i, role in enumerate(role_criteria):
    ttk.Radiobutton(roles_frame, text=role, variable=role_var, value=role).grid(row=i, column=0, sticky="w")

ttk.Button(frame, text="Upload Resume (PDF)", command=process_resume).grid(row=5, column=0, columnspan=2, pady=10)
ttk.Button(frame, text="Clear / Sign Out", command=clear_form).grid(row=6, column=0, columnspan=2, pady=5)

loading_label = ttk.Label(frame, text="", foreground="green")
loading_label.grid(row=7, column=0, columnspan=2)

ttk.Label(frame, text="Parsed Resume Output:").grid(row=8, column=0, columnspan=2, pady=5)
result_text = tk.Text(frame, height=20, wrap=tk.WORD, font=("Courier New", 10))
result_text.grid(row=9, column=0, columnspan=2, sticky="nsew", pady=5)
result_text.config(state=tk.DISABLED)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=result_text.yview)
scrollbar.grid(row=9, column=2, sticky="ns")
result_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
