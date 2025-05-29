import requests
import random
import re

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
            print(f"API Response Status: {response.status_code}")
            
            data = response.json()
            jobs_raw = data.get("data", [])
            print(f"Number of jobs found: {len(jobs_raw)}")

            
            if not jobs_raw:
                print("Using sample job data...")
                return self.get_sample_jobs()

            jobs = []
            for job in jobs_raw:
                description = job.get("job_description", "").lower()
                extracted_skills = self.extract_skills_from_description(description)
                print(f"Job: {job.get('job_title')} - Skills found: {extracted_skills}")
                
                jobs.append({
                    "title": job.get("job_title", "Unknown"),
                    "company": job.get("employer_name", "Unknown"),
                    "location": job.get("job_city", "") + ", " + job.get("job_country", ""),
                    "description": description,
                    "skills": extracted_skills,
                    "applicants": random.randint(5, 30),
                    "url": job.get("job_apply_link", "https://www.google.com")
                })

            return jobs
        except Exception as e:
            print(f"Job API Error: {e}")
            print("Using sample job data due to API error...")
            return self.get_sample_jobs()

    def get_sample_jobs(self):
        
        def get_random_score(score_type):
            if score_type == "low":
                return round(random.uniform(0.1, 0.35), 2)
            elif score_type == "medium":
                return round(random.uniform(0.45, 0.65), 2)
            else:  # high
                return round(random.uniform(0.75, 0.95), 2)

        
        score_types = ["low", "medium", "high", "medium"]  
        random.shuffle(score_types)  # Karıştır

        sample_jobs = [
            {
                "title": "Software Developer Intern",
                "company": "Tech Corp",
                "location": "Remote",
                "description": "Looking for Python and Java developer",
                "skills": ["Python", "Java", "Data Science"],
                "applicants": random.randint(5, 30),
                "url": "https://example.com/job1",
                "score": get_random_score(score_types[0])
            },
            {
                "title": "AI Research Intern",
                "company": "AI Solutions",
                "location": "Remote",
                "description": "AI and ML focused internship",
                "skills": ["Python", "AI", "ML", "Data Science"],
                "applicants": random.randint(5, 30),
                "url": "https://example.com/job2",
                "score": get_random_score(score_types[1])
            },
            {
                "title": "Software Engineering Intern",
                "company": "Software Inc",
                "location": "Remote",
                "description": "Java and Spring Boot development",
                "skills": ["Java", "SQL", "JavaScript"],
                "applicants": random.randint(5, 30),
                "url": "https://example.com/job3",
                "score": get_random_score(score_types[2])
            },
            {
                "title": "Data Science Intern",
                "company": "Data Corp",
                "location": "Remote",
                "description": "Python and Data Science work",
                "skills": ["Python", "Data Science", "SQL"],
                "applicants": random.randint(5, 30),
                "url": "https://example.com/job4",
                "score": get_random_score(score_types[3])
            }
        ]

        
        sorted_jobs = sorted(sample_jobs, key=lambda x: (x["score"] < 0.4, random.random()))
        return sorted_jobs

    def extract_skills_from_description(self, description):
        
        skill_patterns = {
            "Python": r"python|django|flask|fastapi",
            "Java": r"java\b|spring boot|hibernate",
            "C++": r"c\+\+|cpp|c plus plus",
            "HTML": r"html|html5|markup",
            "CSS": r"css|css3|scss|sass|styling",
            "AI": r"ai|artificial intelligence|machine learning|deep learning",
            "ML": r"ml|machine learning|tensorflow|pytorch|scikit",
            "Data Science": r"data science|data analysis|pandas|numpy|statistics",
            "SQL": r"sql|mysql|postgresql|database|oracle",
            "JavaScript": r"javascript|js|node|react|angular|vue"
        }

        found_skills = []
        description = description.lower()
        
        for skill, pattern in skill_patterns.items():
            if re.search(pattern, description):
                found_skills.append(skill)

        return found_skills 