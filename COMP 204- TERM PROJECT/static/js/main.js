document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('cvInput');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const results = document.getElementById('results');

    // Drag and drop handlers
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropZone.classList.add('drag-over');
    }

    function unhighlight(e) {
        dropZone.classList.remove('drag-over');
    }

    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFileSelect, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const file = dt.files[0];
        handleFile(file);
    }

    function handleFileSelect(e) {
        const file = e.target.files[0];
        handleFile(file);
    }

    function handleFile(file) {
        if (file && file.type === 'application/pdf') {
            uploadFile(file);
        } else {
            alert('Please upload a PDF file.');
        }
    }

    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('cv', file);

        try {
            showLoading();
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing your CV.');
        } finally {
            hideLoading();
        }
    }

    function showLoading() {
        dropZone.classList.add('d-none');
        loadingSpinner.classList.remove('d-none');
        results.classList.add('d-none');
    }

    function hideLoading() {
        loadingSpinner.classList.add('d-none');
        results.classList.remove('d-none');
    }

    function displayResults(data) {
        // Display CV info
        document.getElementById('department').textContent = data.cv_info.department;
        document.getElementById('year').textContent = data.cv_info.year;
        
        const skillsContainer = document.getElementById('skills');
        skillsContainer.innerHTML = data.cv_info.skills
            .map(skill => `<span class="skill-tag">${skill}</span>`)
            .join('');

        // Display matched jobs
        const matchedJobsContainer = document.getElementById('matchedJobs');
        matchedJobsContainer.innerHTML = data.matched_jobs
            .map(job => `
                <div class="job-card position-relative fade-in">
                    <span class="match-score">Match: ${job.score}</span>
                    <h4 class="job-title">${job.title}</h4>
                    <div class="job-company">${job.company}</div>
                    <div class="job-location">${job.location}</div>
                    <div class="job-skills">
                        ${job.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                    </div>
                    <div class="mt-3">
                        <a href="${job.url}" target="_blank" class="btn btn-primary">
                            <i class="fas fa-external-link-alt me-2"></i>Apply Now
                        </a>
                    </div>
                </div>
            `)
            .join('');
    }
}); 