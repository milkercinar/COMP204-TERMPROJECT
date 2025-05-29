import fitz
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
import random
import os
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import customtkinter as ctk

# CV PARSER
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

import requests
import random

class JobFetcher:
    def fetch_jobs(self):
        url = "https://jsearch.p.rapidapi.com/search"
        querystring = {
            "query": "intern software",
            "num_pages": "5"
        }

        headers = {
            "X-RapidAPI-Key": "0c5be2b594msh6c03c3bbf846bfep1242c2jsn60e7f51c48b9",
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()
            jobs_raw = data.get("data", [])

            jobs = []
            for job in jobs_raw:
                # Extract skills from description
                skills = self.extract_skills_from_description(job.get("description", ""))
                
                # Calculate base score with more variance
                base_score = 0.2 + (len(skills) / 15)  # Lower base score and skill impact
                
                # Add bonus for relevant keywords in title
                title = job.get("job_title", "").lower()
                if "software" in title or "developer" in title:
                    base_score += random.uniform(0.1, 0.3)  # Random bonus
                if "data" in title and "science" in title:
                    base_score += random.uniform(0.1, 0.25)
                if "machine learning" in title or "ai" in title:
                    base_score += random.uniform(0.15, 0.35)
                if "web" in title or "full stack" in title:
                    base_score += random.uniform(0.05, 0.2)
                
                # Add significant random factor for more variety
                variance = random.uniform(-0.2, 0.2)
                score = min(0.98, max(0.15, base_score + variance))
                
                jobs.append({
                    "title": job.get("job_title", "Unknown"),
                    "company": job.get("employer_name", "Unknown Company"),
                    "skills": skills,
                    "applicants": random.randint(5, 30),
                    "url": job.get("job_apply_link", "https://www.google.com"),
                    "score": round(score, 2)
                })

            # Shuffle the jobs list for random ordering
            random.shuffle(jobs)
            return jobs
        except Exception as e:
            print("Job API Error:", e)
            return self.get_sample_jobs()

    def get_sample_jobs(self):
        sample_jobs = [
            {
                "title": "Software Engineering Intern",
                "company": "Tech Corp",
                "skills": ["Python", "Java", "SQL"],
                "applicants": random.randint(5, 30),
                "url": "https://www.google.com",
                "score": 0.92  # Super Match
            },
            {
                "title": "Data Science Intern",
                "company": "Data Analytics Inc",
                "skills": ["Python", "ML", "SQL"],
                "applicants": random.randint(5, 30),
                "url": "https://www.google.com",
                "score": 0.35  # Low Match
            },
            {
                "title": "Web Development Intern",
                "company": "Web Solutions",
                "skills": ["HTML", "CSS", "JavaScript"],
                "applicants": random.randint(5, 30),
                "url": "https://www.google.com",
                "score": 0.65  # Good Match
            },
            {
                "title": "ML Engineering Intern",
                "company": "AI Research Labs",
                "skills": ["Python", "ML", "AI", "Data Science"],
                "applicants": random.randint(5, 30),
                "url": "https://www.google.com",
                "score": 0.25  # Low Match
            },
            {
                "title": "Backend Developer Intern",
                "company": "Cloud Systems Inc",
                "skills": ["Java", "SQL", "Python"],
                "applicants": random.randint(5, 30),
                "url": "https://www.google.com",
                "score": 0.82  # Super Match
            },
            {
                "title": "Frontend Developer Intern",
                "company": "Digital Solutions",
                "skills": ["JavaScript", "HTML", "CSS"],
                "applicants": random.randint(5, 30),
                "url": "https://www.google.com",
                "score": 0.45  # Medium Match
            },
            {
                "title": "Full Stack Developer Intern",
                "company": "StartupCo",
                "skills": ["Python", "JavaScript", "SQL"],
                "applicants": random.randint(5, 30),
                "url": "https://www.google.com",
                "score": 0.72  # Good Match
            }
        ]
        # Shuffle the sample jobs for random ordering
        random.shuffle(sample_jobs)
        return sample_jobs

    def extract_skills_from_description(self, description):
        keywords = ["Python", "Java", "C++", "HTML", "CSS", "AI", "ML", "Data Science", "SQL", "JavaScript"]
        return [k for k in keywords if k.lower() in description.lower()]


# MATCHER
class InternshipMatcher:
    def __init__(self, cv_data, jobs):
        self.cv_data = cv_data
        self.jobs = jobs

    def match_jobs(self):
        # Sort jobs by score in descending order
        return sorted(self.jobs, key=lambda x: (-x["score"], random.random()))

# GUI
class MatchMeInternGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("MatchMeIntern - AI Internship Matcher")
        self.root.geometry("1000x800")
        
        # Set the color theme and appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Define custom colors
        self.colors = {
            'primary': "#6C5CE7",  # Modern purple
            'secondary': "#00D2D3", # Bright turquoise
            'background': "#0F1729", # Dark navy blue
            'card': "#1A2332",      # Slightly lighter navy
            'text': "#FFFFFF",      # White text
            'subtext': "#A0AEC0"    # Subtle gray for secondary text
        }

        self.file_path = None
        self.cv_info = {}
        self.build_interface()

    def open_url(self, url):
        webbrowser.open(url)

    def build_interface(self):
        # Main container with padding
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create TabView
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True)

        # Create tabs
        self.find_intern_tab = self.tabview.add("Find Intern")
        self.cv_score_tab = self.tabview.add("CV Score")

        # Build Find Intern Tab
        self.build_find_intern_tab()
        
        # Build CV Score Tab
        self.build_cv_score_tab()

    def build_find_intern_tab(self):
        # Profile Section (Left Side)
        self.profile_frame = ctk.CTkFrame(self.find_intern_tab)
        self.profile_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Logo Frame
        logo_frame = ctk.CTkFrame(self.profile_frame, fg_color="transparent")
        logo_frame.pack(pady=(20, 40))

        # Load and display logo
        logo_path = os.path.join("logo", "matchmeinter_logo.png")
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((300, 150), Image.Resampling.LANCZOS)
        self.logo_photo = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(300, 150))
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            image=self.logo_photo,
            text=""
        )
        logo_label.pack()

        # Stats Frame
        self.stats_frame = ctk.CTkFrame(self.profile_frame)
        self.stats_frame.pack(fill="x", padx=20, pady=10)

        # Upload Section
        self.upload_frame = ctk.CTkFrame(self.profile_frame, fg_color="transparent")
        self.upload_frame.pack(fill="x", padx=20, pady=20)

        self.upload_btn = ctk.CTkButton(
            self.upload_frame,
            text="Upload Your CV (PDF)",
            command=self.upload_cv,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color="#5849c2"
        )
        self.upload_btn.pack(fill="x", pady=5)

        self.find_btn = ctk.CTkButton(
            self.upload_frame,
            text="Find Me an Internship!",
            command=self.find_jobs,
            state="disabled",
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=self.colors['secondary'],
            hover_color="#00b3b3",
            text_color="#000000"
        )
        self.find_btn.pack(fill="x", pady=5)

        # Results Section (Right Side)
        self.results_frame = ctk.CTkFrame(self.find_intern_tab, fg_color=self.colors['background'])
        self.results_frame.pack(side="right", fill="both", expand=True, padx=10)

        # Results Header
        self.results_header = ctk.CTkLabel(
            self.results_frame,
            text="Matched Internships",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=self.colors['text']
        )
        self.results_header.pack(pady=20)

        # Results Scrollable Frame
        self.results_scroll = ctk.CTkScrollableFrame(
            self.results_frame,
            label_text="Results"
        )
        self.results_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def build_cv_score_tab(self):
        # Left side - Upload and Analysis Section
        left_frame = ctk.CTkFrame(self.cv_score_tab)
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Upload Section
        upload_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        upload_frame.pack(fill="x", padx=20, pady=20)

        self.cv_upload_btn = ctk.CTkButton(
            upload_frame,
            text="Upload CV for Analysis (PDF)",
            command=self.upload_cv_for_analysis,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color="#5849c2"
        )
        self.cv_upload_btn.pack(fill="x", pady=5)

        self.analyze_btn = ctk.CTkButton(
            upload_frame,
            text="Analyze CV",
            command=self.analyze_cv,
            state="disabled",
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=self.colors['secondary'],
            hover_color="#00b3b3",
            text_color="#000000"
        )
        self.analyze_btn.pack(fill="x", pady=5)

        # Right side - Results Section
        right_frame = ctk.CTkFrame(self.cv_score_tab, fg_color=self.colors['background'])
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        # Score Display
        self.score_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        self.score_frame.pack(fill="x", padx=20, pady=20)

        self.score_label = ctk.CTkLabel(
            self.score_frame,
            text="ATS Compatibility Score",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=self.colors['text']
        )
        self.score_label.pack(pady=10)

        self.score_value = ctk.CTkLabel(
            self.score_frame,
            text="--",
            font=ctk.CTkFont(family="Segoe UI", size=48, weight="bold"),
            text_color=self.colors['secondary']
        )
        self.score_value.pack(pady=10)

        # Analysis Results
        self.analysis_frame = ctk.CTkScrollableFrame(
            right_frame,
            label_text="Analysis Results",
            fg_color=self.colors['background']
        )
        self.analysis_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Sections for different analysis results
        self.missing_sections = ctk.CTkTextbox(
            self.analysis_frame,
            height=100,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=self.colors['card']
        )
        self.missing_sections.pack(fill="x", pady=5)
        self.missing_sections.insert("1.0", "Missing Sections will appear here...")
        self.missing_sections.configure(state="disabled")

        self.improvement_suggestions = ctk.CTkTextbox(
            self.analysis_frame,
            height=100,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=self.colors['card']
        )
        self.improvement_suggestions.pack(fill="x", pady=5)
        self.improvement_suggestions.insert("1.0", "Improvement suggestions will appear here...")
        self.improvement_suggestions.configure(state="disabled")

        self.success_points = ctk.CTkTextbox(
            self.analysis_frame,
            height=100,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=self.colors['card']
        )
        self.success_points.pack(fill="x", pady=5)
        self.success_points.insert("1.0", "Strong points will appear here...")
        self.success_points.configure(state="disabled")

    def upload_cv(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")],
            title="Select Your CV"
        )
        if self.file_path:
            self.status_bar.configure(text="Processing CV...")
            parser = CVParser(self.file_path)
            self.cv_info = parser.extract_info()
            
            # Update Stats
            self.update_profile_stats()
            
            self.find_btn.configure(state="normal")
            self.status_bar.configure(text="CV uploaded successfully!")

    def update_profile_stats(self):
        # Clear existing stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Department
        dept_label = ctk.CTkLabel(
            self.stats_frame,
            text="Department",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=self.colors['subtext']
        )
        dept_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        dept_value = ctk.CTkLabel(
            self.stats_frame,
            text=self.cv_info['department'],
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=self.colors['text']
        )
        dept_value.pack(anchor="w", padx=10)

        # Year
        year_label = ctk.CTkLabel(
            self.stats_frame,
            text="Year",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=self.colors['subtext']
        )
        year_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        year_value = ctk.CTkLabel(
            self.stats_frame,
            text=self.cv_info['year'],
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=self.colors['text']
        )
        year_value.pack(anchor="w", padx=10)

        # Skills
        skills_label = ctk.CTkLabel(
            self.stats_frame,
            text="Skills",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=self.colors['subtext']
        )
        skills_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        skills_frame = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        skills_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        for skill in self.cv_info['skills']:
            skill_tag = ctk.CTkButton(
                skills_frame,
                text=skill,
                height=28,
                width=90,
                corner_radius=8,
                font=ctk.CTkFont(family="Segoe UI", size=12),
                fg_color=self.colors['secondary'],
                hover_color=self.colors['secondary'],
                text_color="#000000"
            )
            skill_tag.pack(side="left", padx=2, pady=2)

    def create_job_card(self, job):
        # Create a card frame for each job
        card = ctk.CTkFrame(self.results_scroll, fg_color=self.colors['card'])
        card.pack(fill="x", padx=10, pady=8)

        # Job Title and Company
        title_frame = ctk.CTkFrame(card, fg_color="transparent")
        title_frame.pack(fill="x", padx=15, pady=(15, 5))

        title = ctk.CTkLabel(
            title_frame,
            text=f"{job['title']}",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=self.colors['text']
        )
        title.pack(anchor="w")

        company = ctk.CTkLabel(
            title_frame,
            text=f"{job['company']}",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=self.colors['subtext']
        )
        company.pack(anchor="w")

        # Match Score with progress bar
        score_frame = ctk.CTkFrame(card, fg_color="transparent")
        score_frame.pack(fill="x", padx=15, pady=10)
        
        # Determine score color and text
        if job['score'] < 0.4:  # Low score
            score_color = "#FF4B4B"  # Red
            score_text = "Low Match"
        elif job['score'] < 0.7:  # Medium score
            score_color = "#FFA500"  # Orange/Yellow
            score_text = "Good Match"
        else:  # High score
            score_color = "#00D2D3"  # Use secondary color for high scores
            score_text = "Great Match"
        
        score_label = ctk.CTkLabel(
            score_frame,
            text=f"{score_text} ({job['score']:.2f})",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=score_color
        )
        score_label.pack(side="left")

        score_bar = ctk.CTkProgressBar(
            score_frame,
            width=200,
            height=8,
            corner_radius=4
        )
        score_bar.pack(side="right", padx=10)
        score_bar.configure(
            progress_color=score_color,
            fg_color=self.colors['background'],
            border_color=score_color
        )
        score_bar.set(job['score'])

        # Skills Section
        if job.get("skills"):
            skills_frame = ctk.CTkFrame(card, fg_color="transparent")
            skills_frame.pack(fill="x", padx=15, pady=5)
            
            # Required Skills Label
            skills_label = ctk.CTkLabel(
                skills_frame,
                text="Required Skills:",
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color=self.colors['subtext']
            )
            skills_label.pack(anchor="w", pady=(0, 5))
            
            # Skills Container
            skills_container = ctk.CTkFrame(skills_frame, fg_color="transparent")
            skills_container.pack(fill="x")
            
            # Display skills
            for skill in job["skills"]:
                skill_tag = ctk.CTkButton(
                    skills_container,
                    text=skill,
                    height=28,
                    width=90,
                    corner_radius=8,
                    font=ctk.CTkFont(family="Segoe UI", size=12),
                    fg_color=self.colors['primary'],
                    hover_color=self.colors['primary'],
                    text_color=self.colors['text']
                )
                skill_tag.pack(side="left", padx=2, pady=2)

        # Apply Button
        apply_btn = ctk.CTkButton(
            card,
            text="Apply Now",
            command=lambda url=job['url']: self.open_url(url),
            width=130,
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color="#5849c2"
        )
        apply_btn.pack(anchor="e", padx=15, pady=15)

    def find_jobs(self):
        if not self.file_path or not self.cv_info:
            messagebox.showwarning("No CV", "Please upload a CV first.")
            return

        self.status_bar.configure(text="Searching for internships...")
        
        # Clear existing results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()

        fetcher = JobFetcher()
        jobs = fetcher.fetch_jobs()
        matcher = InternshipMatcher(self.cv_info, jobs)
        matched = matcher.match_jobs()

        # Create job cards
        for job in matched:
            self.create_job_card(job)

        self.status_bar.configure(text="Found matching internships!")

    def upload_cv_for_analysis(self):
        self.cv_file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")],
            title="Select Your CV for Analysis"
        )
        if self.cv_file_path:
            self.analyze_btn.configure(state="normal")
            messagebox.showinfo("Success", "CV uploaded successfully! Click 'Analyze CV' to start analysis.")

    def analyze_cv(self):
        if not hasattr(self, 'cv_file_path') or not self.cv_file_path:
            messagebox.showerror("Error", "Please upload a CV first!")
            return

        # Create CV parser instance
        parser = CVParser(self.cv_file_path)
        cv_text = parser.extract_text()
        cv_text_lower = cv_text.lower()

        # Initialize score components and feedback lists
        scores = {
            'keyword_match': 0,      # 50%
            'technical_skills': 0,   # 15%
            'experience_match': 0,   # 15%
            'education_match': 0,    # 10%
            'format_quality': 0      # 10%
        }
        missing = []
        improvements = []
        successes = []

        # 1. Check for basic sections and their headers (clear section headers)
        section_headers = {
            'experience': ['work experience', 'professional experience', 'experience'],
            'education': ['education', 'academic background'],
            'projects': ['projects', 'personal projects', 'project experience'],
            'skills': ['skills', 'technical skills', 'core competencies'],
            'certifications': ['certifications', 'certificates', 'professional certifications']
        }

        found_sections = set()
        for section, headers in section_headers.items():
            if any(header in cv_text_lower for header in headers):
                found_sections.add(section)
                successes.append(f"✅ Clear '{section.title()}' section header found")
            else:
                improvements.append(f"💡 Add a clear '{section.title()}' section header")

        # 2. Check for keyword matching (50% weight)
        tech_keywords = {
            'languages': ['python', 'java', 'javascript', 'c++', 'typescript'],
            'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'spring'],
            'databases': ['sql', 'mongodb', 'postgresql', 'mysql'],
            'tools': ['git', 'docker', 'kubernetes', 'aws', 'azure'],
            'concepts': ['agile', 'ci/cd', 'testing', 'api', 'rest']
        }

        keyword_matches = []
        for category, keywords in tech_keywords.items():
            found = [kw for kw in keywords if kw in cv_text_lower]
            if found:
                keyword_matches.extend(found)

        keyword_score = min(len(keyword_matches) * 5, 50)  # Max 50%
        scores['keyword_match'] = keyword_score

        if keyword_matches:
            successes.append(f"✅ Found relevant keywords: {', '.join(keyword_matches).title()}")
        else:
            improvements.append("❌ Add more relevant technical keywords matching the job requirements")

        # 3. Check technical skills format (15% weight)
        if 'skills' in found_sections:
            skills_lines = [line for line in cv_text.split('\n') if 'skills' in line.lower()]
            has_bullet_points = any('•' in line or '-' in line for line in cv_text.split('\n'))
            if has_bullet_points:
                scores['technical_skills'] = 15
                successes.append("✅ Skills are properly listed with bullet points")
            else:
                improvements.append("❌ List technical skills clearly with bullet points")

        # 4. Check experience/location match (15% weight)
        experience_patterns = [
            r'\d+\s*(?:year|yr)s?\s+(?:of\s+)?experience',
            r'(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}',
            r'\d{4}\s*-\s*(?:present|current|now|\d{4})'
        ]
        
        has_dates = any(re.search(pattern, cv_text_lower) for pattern in experience_patterns)
        if has_dates:
            scores['experience_match'] = 15
            successes.append("✅ Clear experience timeline found")
        else:
            improvements.append("❌ Add clear dates and duration for experiences")

        # 5. Check education format (10% weight)
        education_patterns = [
            r'bachelor|master|phd|bs|ms|b\.s\.|m\.s\.',
            r'university|college|institute',
            r'20\d\d\s*-\s*20\d\d|20\d\d'
        ]
        
        has_education = any(re.search(pattern, cv_text_lower) for pattern in education_patterns)
        if has_education:
            scores['education_match'] = 10
            successes.append("✅ Education details properly formatted")
        else:
            improvements.append("❌ Add clear education details with dates")

        # 6. Check format quality (10% weight)
        format_issues = []
        
        # Check for complex formatting
        if len(cv_text.split('\n')) > 100:  # Too many lines
            format_issues.append("Too many lines - simplify format")
        
        # Check for scanned PDF
        if len(cv_text.strip()) < 100:  # Very little text extracted
            format_issues.append("PDF might be scanned/image-based")
        
        # Check for common formatting issues
        if cv_text.count('  ') > 10:  # Multiple spaces
            format_issues.append("Inconsistent spacing")
        
        if not format_issues:
            scores['format_quality'] = 10
            successes.append("✅ Clean, ATS-friendly formatting")
        else:
            improvements.extend([f"❌ Format issue: {issue}" for issue in format_issues])

        # Calculate final score with weights
        final_score = sum(scores.values())

        # Update GUI with results
        self.score_value.configure(text=f"{final_score}%")
        
        # Update missing sections
        self.missing_sections.configure(state="normal")
        self.missing_sections.delete("1.0", "end")
        missing_text = "Missing Sections:\n"
        if not found_sections:
            missing_text += "❌ No clear section headers found\n"
        for section in section_headers.keys():
            if section not in found_sections:
                missing_text += f"❌ Missing {section.title()} section\n"
        self.missing_sections.insert("1.0", missing_text)
        self.missing_sections.configure(state="disabled")

        # Update improvements
        self.improvement_suggestions.configure(state="normal")
        self.improvement_suggestions.delete("1.0", "end")
        self.improvement_suggestions.insert("1.0", "Improvement Suggestions:\n" + "\n".join(improvements))
        self.improvement_suggestions.configure(state="disabled")

        # Update successes
        self.success_points.configure(state="normal")
        self.success_points.delete("1.0", "end")
        self.success_points.insert("1.0", "Strong Points:\n" + "\n".join(successes))
        self.success_points.configure(state="disabled")

        # Color the score based on value
        if final_score < 40:
            self.score_value.configure(text_color="#FF4B4B")  # Red
        elif final_score < 70:
            self.score_value.configure(text_color="#FFA500")  # Orange
        else:
            self.score_value.configure(text_color="#00D2D3")  # Turquoise

    def run(self):
        self.root.mainloop()

# LAUNCH APP
if __name__ == "__main__":
    MatchMeInternGUI().run()