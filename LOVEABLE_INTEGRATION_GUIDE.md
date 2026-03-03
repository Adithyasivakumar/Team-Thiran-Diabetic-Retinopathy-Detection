# API Configuration Guide for Loveable Frontend

## Backend API Details

### Base URL
- **Development:** `http://localhost:5000`
- **Production:** `https://your-render-url.onrender.com`

### Authentication
- Session-based (cookies)
- Login endpoint: `POST /login`
- Credentials: `demo_user` / `demo_password`

### API Endpoints

#### 1. Image Prediction
```
Endpoint: POST /api/predict
Authentication: Required (login first)
Content-Type: multipart/form-data

Request:
{
  "file": <image_file>  # Key name is important!
}

Response:
{
  "success": true,
  "class": "No DR",  // or "Mild", "Moderate", "Severe", "Proliferative"
  "confidence": 0.95,
  "class_id": 0,
  "timestamp": "2026-03-03 10:47:00"
}
```

#### 2. Generate Report
```
Endpoint: POST /api/generate-report
Authentication: Required
Content-Type: application/json

Request:
{
  "patient_name": "John Doe",
  "age": 45,
  "class": "Moderate",
  "confidence": 0.92,
  "uploaded_file": "filename.jpg",
  "clinical_notes": "Optional notes"
}

Response:
{
  "success": true,
  "report_id": "DR-Test-Patient-20260303142635",
  "message": "Report generated successfully"
}
```

#### 3. Download Report
```
Endpoint: GET /api/download-report/<report_id>
Authentication: Required
Response: PDF file (binary)

Example URL:
/api/download-report/DR-Test-Patient-20260303142635
```

---

## Risk Indicator Logic

Map the `class` field to risk levels:

| Class | Risk Level | Color |
|-------|-----------|-------|
| No DR | Low | 🟢 Green |
| Mild | Low | 🟢 Green |
| Moderate | Medium | 🟡 Yellow |
| Severe | High | 🔴 Red |
| Proliferative | High | 🔴 Red |

---

## Environment Variables (For Loveable)

Create a `.env.local` file in your Loveable React app:

```env
VITE_API_BASE_URL=http://localhost:5000
VITE_API_TIMEOUT=30000
VITE_MAX_FILE_SIZE=50000000
VITE_ALLOWED_FORMATS=jpg,jpeg,png,bmp,tiff
```

---

## File Upload Details

**IMPORTANT:** The backend expects:
```javascript
const formData = new FormData();
formData.append('file', imageFile);  // Key must be 'file'

fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  body: formData,
  credentials: 'include'  // Important for cookies
})
```

---

## Session & Authentication

1. Login creates a session cookie
2. All subsequent API calls must include `credentials: 'include'`
3. CORS is configured to allow credentials
4. Session timeout: 24 hours

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid file) |
| 401 | Not authenticated (login required) |
| 403 | Forbidden (session expired) |
| 500 | Server error |

---

## Test Login Credentials

```
Username: demo_user
Password: demo_password
```

---

## Loveable Prompts to Use

### Initial UI Build Prompt:
```
"Build a professional medical dashboard for Diabetic Retinopathy detection. 
I have an existing Flask API at http://localhost:5000. 

Create a UI with:
1. A modern login form
2. Drag-and-drop image uploader that sends to /api/predict
3. Results card showing Class and Confidence
4. Risk indicator (Low/Medium/High based on class)
5. Sidebar for patient history
6. Button to generate PDF report via /api/generate-report
7. Professional healthcare color scheme (teal/blue/white)

Use React hooks for state management. The API uses multipart/form-data 
with key name 'file' for images."
```

### Configuration Prompt:
```
"Create an API configuration file that uses environment variables. 
Development: http://localhost:5000
Production: Read from VITE_API_BASE_URL env variable.

Ensure all fetch calls include credentials: 'include' for session cookies."
```

### File Upload Prompt:
```
"The image uploader must:
1. Accept JPG, PNG, BMP, TIFF files
2. Max size: 50MB
3. Send as multipart/form-data with key 'file'
4. Show upload progress
5. Display error if file format is invalid"
```

### Response Mapping Prompt:
```
"Backend returns JSON: {\"class\": \"Moderate\", \"confidence\": 0.92}

Map to risk levels:
- No DR / Mild = Low (green)
- Moderate = Medium (yellow)  
- Severe / Proliferative = High (red)

Show the risk badge next to confidence score."
```

---

## Troubleshooting for Loveable

### "API returns 401 Unauthorized"
→ You forgot to login first. Loveable UI must login before calling /api/predict

### "CORS Error"
→ Backend is not running. Make sure Flask is running on http://localhost:5000

### "File upload fails"
→ Check the FormData key is 'file' (case-sensitive)

### "No results after upload"
→ Check browser console for errors. Verify backend is processing the image.

---

## Deployment Checklist

**Backend (Render.com):**
- [ ] Push to GitHub
- [ ] Deploy to Render
- [ ] Set environment variables
- [ ] Test /api/predict endpoint

**Frontend (Loveable → Netlify/Vercel):**
- [ ] Create new GitHub repo: DR-Detection-Frontend
- [ ] Connect to Netlify/Vercel
- [ ] Set VITE_API_BASE_URL = your Render URL
- [ ] Deploy

---

## Local Development Commands

```bash
# Terminal 1: Backend (in your current repo)
source venv/bin/activate
python -m flask run

# Terminal 2: Frontend (in new DR-Detection-Frontend repo)
npm install
npm run dev

# Result: Backend on http://localhost:5000, Frontend on http://localhost:5173
```
