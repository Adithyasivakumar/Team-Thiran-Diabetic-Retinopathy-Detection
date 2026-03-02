/*
  Team Thiran - Web Interface JavaScript
  Handles file uploads, predictions, and report generation
*/

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const resultsCard = document.getElementById('resultsCard');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');
const previewImage = document.getElementById('previewImage');
const reportModal = document.getElementById('reportModal');
const errorAlert = document.getElementById('errorAlert');

// Current analysis data
let currentAnalysis = {
    prediction: null,
    imagePath: null,
    confidence: null,
    report: null,
    reportId: null
};

// ============================================================================
// FILE UPLOAD HANDLING
// ============================================================================

if (uploadArea) {
    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
}

function handleFileSelect(file) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/bmp', 'image/tiff'];
    if (!validTypes.includes(file.type)) {
        showError('Invalid file format. Please upload: JPG, PNG, BMP, or TIFF');
        return;
    }

    // Validate file size (max 50MB)
    if (file.size > 50 * 1024 * 1024) {
        showError('File size too large. Maximum 50 MB allowed.');
        return;
    }

    // Clear stale state when a new image is selected
    currentAnalysis.report = null;
    currentAnalysis.reportId = null;

    // Create FormData and upload
    const formData = new FormData();
    formData.append('file', file);

    uploadImage(formData);
}

// ============================================================================
// IMAGE UPLOAD & PREDICTION
// ============================================================================

function uploadImage(formData) {
    // Show progress
    progressContainer.classList.remove('hidden');
    resultsCard.classList.add('hidden');
    errorAlert.classList.add('hidden');

    // Simulate progress
    let progress = 0;
    const interval = setInterval(() => {
        if (progress < 90) {
            progress += Math.random() * 30;
            progressBar.style.width = Math.min(progress, 90) + '%';
        }
    }, 200);

    // Send prediction request
    fetch('/api/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Prediction failed');
            });
        }
        return response.json();
    })
    .then(data => {
        clearInterval(interval);
        progressBar.style.width = '100%';

        // Update current analysis
        currentAnalysis.prediction = data.prediction;
        currentAnalysis.imagePath = data.image_path;

        // Display results
        setTimeout(() => {
            displayResults(data);
            progressContainer.classList.add('hidden');
            resultsCard.classList.remove('hidden');
        }, 500);
    })
    .catch(error => {
        clearInterval(interval);
        progressContainer.classList.add('hidden');
        showError(error.message);
    });
}

function displayResults(data) {
    // Display prediction results
    if (data.thumbnail) {
        previewImage.src = data.thumbnail;
    }

    // Store confidence for later use
    currentAnalysis.confidence = data.confidence;

    // Severity information
    const severityLevels = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative'];
    const severityText = severityLevels[data.prediction];

    // Update severity badge
    const severityBadge = document.getElementById('severityBadge');
    severityBadge.textContent = '⚕️ ' + severityText;
    severityBadge.className = 'severity-badge severity-' + data.prediction;

    // Update info items
    document.getElementById('severityLevel').textContent = data.prediction + '/4';
    document.getElementById('classification').textContent = severityText;
    document.getElementById('confidence').textContent = data.confidence;

    // Show patient form and generate report button
    const patientForm = document.getElementById('patientForm');
    const generateBtn = document.getElementById('generateReportBtn');
    if (patientForm) patientForm.style.display = 'block';
    if (generateBtn) generateBtn.style.display = 'inline-block';

    // Hide upload area
    uploadArea.style.display = 'none';

    console.log('Analysis complete:', data);
}

// ============================================================================
// REPORT GENERATION
// ============================================================================

function generateReport() {
    if (currentAnalysis.prediction === null) {
        showError('No analysis available');
        return;
    }

    const patientInfo = {
        name: document.getElementById('patientName').value || 'Anonymous',
        email: document.getElementById('patientEmail').value || '',
        phone: document.getElementById('patientPhone').value || '',
        age: document.getElementById('patientAge').value || '',
        gender: document.getElementById('patientGender').value || ''
    };

    // Show loading
    const reportStatus = document.getElementById('reportStatus');
    const reportStatusText = document.getElementById('reportStatusText');
    reportStatus.classList.remove('hidden');
    if (reportStatusText) {
        reportStatusText.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating report and preparing PDF...';
    }

    fetch('/api/generate-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            prediction: currentAnalysis.prediction,
            confidence: currentAnalysis.confidence,
            patient_info: patientInfo,
            image_path: currentAnalysis.imagePath
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Report generation failed');
            });
        }
        return response.json();
    })
    .then(data => {
        currentAnalysis.report = data.report;
        currentAnalysis.reportId = data.report_id || null;
        reportStatus.classList.add('hidden');

        // Show verification modal
        showReportModal(data.report);
    })
    .catch(error => {
        reportStatus.classList.add('hidden');
        showError(error.message);
    });
}

function showReportModal(report) {
    const reportModalBody = document.getElementById('reportModalBody');

    // Extract data from nested structure returned by backend
    const patientName = report.patient?.name || 'Not provided';
    const patientAge = report.patient?.age || 'Not provided';
    const patientGender = report.patient?.gender || 'Not specified';
    const drLevel = report.findings?.severity_level !== undefined ? report.findings.severity_level : 'N/A';
    const classification = report.findings?.classification || 'Unknown';
    const confidence = report.findings?.confidence || 'N/A';
    const clinicalFindings = report.clinical_assessment || 'No assessment available';

    // Handle recommendations - could be string or array
    let recommendationsHTML = '';
    if (Array.isArray(report.recommendations)) {
        recommendationsHTML = report.recommendations.map(rec => `<li>${rec}</li>`).join('');
    } else if (typeof report.recommendations === 'string') {
        recommendationsHTML = `<li>${report.recommendations}</li>`;
    } else if (Array.isArray(report.next_steps)) {
        // Fallback to next_steps if recommendations not available
        recommendationsHTML = report.next_steps.map(step => `<li>${step}</li>`).join('');
    }

    // Format report HTML with improved layout
    const reportHTML = `
        <div style="font-size: 0.95rem; line-height: 1.8; color: var(--text-color);">
            
            <div style="text-align: center; background: linear-gradient(135deg, var(--primary-color), #2563eb); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <h5 style="margin: 0; font-weight: 700;">🏥 Team Thiran Medical Report</h5>
                <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">Diabetic Retinopathy Detection System</p>
            </div>

            <!-- Patient & Report Info Section -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid var(--primary-color);">
                    <p style="margin: 0 0 8px 0; font-weight: 600; color: var(--text-secondary); font-size: 0.85rem;">REPORT ID</p>
                    <p style="margin: 0; font-weight: 700; color: var(--primary-color); word-break: break-all;">${report.report_id}</p>
                </div>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid var(--secondary-color);">
                    <p style="margin: 0 0 8px 0; font-weight: 600; color: var(--text-secondary); font-size: 0.85rem;">DATE & TIME</p>
                    <p style="margin: 0; font-weight: 700;">${report.report_date}</p>
                </div>
            </div>

            <!-- Patient Information Section -->
            <div style="background: #f0f4f8; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h6 style="margin: 0 0 12px 0; color: var(--primary-color); font-weight: 700; font-size: 1rem;">👤 Patient Information</h6>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div>
                        <p style="margin: 0 0 4px 0; font-weight: 600; color: var(--text-secondary); font-size: 0.85rem;">PATIENT NAME</p>
                        <p style="margin: 0; font-weight: 600;">${patientName}</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 4px 0; font-weight: 600; color: var(--text-secondary); font-size: 0.85rem;">AGE / GENDER</p>
                        <p style="margin: 0; font-weight: 600;">${patientAge} years / ${patientGender}</p>
                    </div>
                </div>
            </div>

            <!-- DR Severity Assessment Section -->
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 20px;">
                <h6 style="margin: 0 0 12px 0; color: #856404; font-weight: 700; font-size: 1rem;">⚕️ Diabetic Retinopathy Assessment</h6>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px;">
                    <div>
                        <p style="margin: 0 0 4px 0; font-weight: 600; color: #856404; font-size: 0.85rem;">SEVERITY LEVEL</p>
                        <p style="margin: 0; font-weight: 700; font-size: 1.1rem; color: #856404;">${drLevel}/4</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 4px 0; font-weight: 600; color: #856404; font-size: 0.85rem;">CLASSIFICATION</p>
                        <p style="margin: 0; font-weight: 700; font-size: 1.1rem;">${classification}</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 4px 0; font-weight: 600; color: #856404; font-size: 0.85rem;">CONFIDENCE</p>
                        <p style="margin: 0; font-weight: 700; font-size: 1.1rem; color: var(--info-color);">${confidence}</p>
                    </div>
                </div>
            </div>

            <!-- Clinical Findings -->
            <div style="background: #e7f3ff; padding: 15px; border-radius: 8px; border-left: 4px solid var(--info-color); margin-bottom: 20px;">
                <h6 style="margin: 0 0 10px 0; color: #0564b0; font-weight: 700; font-size: 1rem;">📋 Clinical Findings</h6>
                <p style="margin: 0; color: #0564b0; line-height: 1.6;">${clinicalFindings}</p>
            </div>

            <!-- Recommendations Section -->
            <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; margin-bottom: 20px;">
                <h6 style="margin: 0 0 12px 0; color: #155724; font-weight: 700; font-size: 1rem;">✅ Medical Recommendations</h6>
                <ul style="margin: 0; padding-left: 20px; color: #155724;">
                    ${recommendationsHTML}
                </ul>
            </div>

            <!-- Disclaimer -->
            <div style="background: #f8d7da; padding: 12px; border-radius: 8px; border-left: 4px solid #dc3545; margin-bottom: 0;">
                <p style="margin: 0; color: #721c24; font-weight: 600; font-size: 0.9rem;">
                    ⚠️ IMPORTANT DISCLAIMER
                </p>
                <p style="margin: 5px 0 0 0; color: #721c24; font-size: 0.85rem; line-height: 1.5;">
                    This is an AI-assisted screening report and should NOT be used as a substitute for professional medical diagnosis. Always consult a qualified ophthalmologist or eye care specialist for final diagnosis and treatment decisions.
                </p>
            </div>
        </div>
    `;

    reportModalBody.innerHTML = reportHTML;
    reportModal.classList.add('show');
}

function downloadReport() {
    if (!currentAnalysis.reportId) {
        showError('Report is not ready for download. Please generate the report again.');
        return;
    }

    window.location.href = `/api/download-report/${encodeURIComponent(currentAnalysis.reportId)}`;
}

function finalizeAnalysis() {
    closeModal();
    showSuccess('✅ Analysis completed successfully. You can start a new case now.');
    resetAnalysis();
}

// ============================================================================
// MODAL & UI UTILITIES
// ============================================================================

function closeModal() {
    reportModal.classList.remove('show');
}

function resetAnalysis() {
    // Reset all form data
    fileInput.value = '';
    resultsCard.classList.add('hidden');
    progressContainer.classList.add('hidden');
    uploadArea.style.display = 'flex';
    errorAlert.classList.add('hidden');
    
    const patientForm = document.getElementById('patientForm');
    const generateBtn = document.getElementById('generateReportBtn');
    if (patientForm) patientForm.style.display = 'none';
    if (generateBtn) generateBtn.style.display = 'none';
    
    document.getElementById('patientName').value = '';
    document.getElementById('patientEmail').value = '';
    document.getElementById('patientPhone').value = '';
    document.getElementById('patientAge').value = '';
    document.getElementById('patientGender').value = '';
    previewImage.src = '';

    // Reset analysis data
    currentAnalysis = {
        prediction: null,
        imagePath: null,
        confidence: null,
        report: null,
        reportId: null
    };
    
    // Scroll back to upload area
    uploadArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showError(message) {
    errorAlert.classList.remove('hidden');
    document.getElementById('errorText').textContent = message;
    errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function showSuccess(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show';
    alert.style = 'margin-top: 20px; border-left: 4px solid #28a745;';
    alert.innerHTML = `
        <i class="fas fa-check-circle"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Try to find container-fluid first, then fall back to container
    const container = document.querySelector('.container-fluid') || document.querySelector('.container');

    if (container) {
        container.prepend(alert);
    } else if (document.body) {
        // Fallback: insert at the top of the body if no container found
        document.body.prepend(alert);
    }
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    if (e.target === reportModal) {
        closeModal();
    }
});

// Prevent default drag behavior on page
document.addEventListener('dragover', (e) => {
    e.preventDefault();
});

document.addEventListener('drop', (e) => {
    e.preventDefault();
});
