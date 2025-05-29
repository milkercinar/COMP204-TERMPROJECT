from flask import Flask, render_template, request, jsonify
import fitz
import re
from werkzeug.utils import secure_filename
import os
from cv_parser import CVParser
from job_fetcher import JobFetcher
from internship_matcher import InternshipMatcher

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'cv' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['cv']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Parse CV
    parser = CVParser(filepath)
    cv_info = parser.extract_info()
    
    # Fetch jobs and match
    fetcher = JobFetcher()
    jobs = fetcher.fetch_jobs()
    matcher = InternshipMatcher(cv_info, jobs)
    matched_jobs = matcher.match_jobs()
    
    # Clean up uploaded file
    os.remove(filepath)
    
    return jsonify({
        'cv_info': cv_info,
        'matched_jobs': matched_jobs
    })

if __name__ == '__main__':
    app.run(debug=True) 