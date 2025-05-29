class InternshipMatcher:
    def __init__(self, cv_data, jobs):
        self.cv_data = cv_data
        self.jobs = jobs

    def match_jobs(self):
        matched_jobs = []
        cv_skills = set(skill.lower() for skill in self.cv_data.get("skills", []))

        for job in self.jobs:
            job_skills = set(skill.lower() for skill in job["skills"])
            match_score = len(cv_skills.intersection(job_skills))
            competition_score = 1 / (job["applicants"] + 1)
            total_score = match_score * competition_score
            job["score"] = round(total_score, 3)
            matched_jobs.append(job)

        return sorted(matched_jobs, key=lambda x: x["score"], reverse=True) 