import fitz
import re

class CVParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = ""

    def extract_text(self):
        with fitz.open(self.pdf_path) as doc:
            self.text = "\n".join(page.get_text() for page in doc)
        return self.text

    def extract_info(self):
        data = {}
        self.extract_text()

        year_match = re.search(r'\b(20[1-3][0-9])\b', self.text)
        skill_keywords = ["python", "java", "c++", "html", "css", "ai", "ml", "data science", "sql", "javascript"]
        department_keywords = [
            "computer engineering", "software engineering", 
            "electrical engineering", "data science", "informatics"
        ]

        skills = []
        for word in skill_keywords:
            if word in self.text.lower():
                skills.append(word.title())

        department = "Unknown"
        for dept in department_keywords:
            if dept in self.text.lower():
                department = dept.title()
                break

        data['year'] = year_match.group(1) if year_match else "Unknown"
        data['skills'] = list(set(skills))
        data['department'] = department
        return data 