<div align="center">

# 🩺 Retinal AI – Diabetic Retinopathy Detection Network
### _AI-Powered Retinal Blindness Detection System (Tamil Nadu Network)_

</div>

---

## 📋 Table of Contents
- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
- [How to Use](#how-to-use)
- [Model Details](#model-details)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Doctors Directory](#doctors-directory)
- [Future Enhancements](#future-enhancements)
- [Team](#team)
- [Acknowledgments](#acknowledgments)

---

## 🖼️ GUI Snapshots

<div align="center">

<img width="1470" height="956" alt="Application Screenshot 1" src="https://github.com/user-attachments/assets/446b9c47-e108-4198-89e3-70cf491768c6" />

<img width="1470" height="956" alt="Application Screenshot 2" src="https://github.com/user-attachments/assets/1d4b7cd6-90ce-4d25-b10b-c010bbc49e6b" />

<img width="1470" height="956" alt="Application Screenshot 3" src="https://github.com/user-attachments/assets/39edf0e3-bef1-41c1-94bf-2ae669ca6476" />

</div>

---

## 🌌 Overview

**Retinal AI** is a deep learning–based system designed to detect and classify **Diabetic Retinopathy (DR)** severity from retinal fundus images. It uses **ResNet-based CNN models (PyTorch)** and a **modern Tkinter GUI** with a dark gradient theme for a professional hospital interface.

The system allows clinicians and users to:
- Upload retinal fundus images for analysis
- Get real-time AI-powered DR severity predictions
- View detailed diagnostic reports
- Access verified ophthalmologists across Tamil Nadu
- Provide feedback for continuous improvement

---

## 💡 Problem Statement

> **Diabetic Retinopathy (DR) is the leading cause of preventable blindness in adults.**

### Key Challenges:
- Manual diagnosis requires trained ophthalmologists and is time-consuming
- Lack of experts in rural and remote areas delays early detection and treatment
- Early detection significantly improves patient outcomes and prevents permanent vision loss
- AI-based screening systems can reduce diagnostic burden and democratize healthcare access

---

## 🚀 Solution Overview

A **ResNet-based CNN** model (trained on APTOS 2019 dataset) predicts DR severity from 0–4:

| Label | Condition | Description |
|:-----:|:-----------|:------------|
| 0 | 🟢 No DR | No diabetic retinopathy detected |
| 1 | 🟡 Mild | Mild non-proliferative diabetic retinopathy |
| 2 | 🟠 Moderate | Moderate non-proliferative diabetic retinopathy |
| 3 | 🔴 Severe | Severe non-proliferative diabetic retinopathy |
| 4 | ⚫ Proliferative DR | Proliferative diabetic retinopathy (highest severity) |

Users can log in, upload retinal images, get diagnostic predictions, and contact nearby ophthalmologists for follow-up care.

---

## 🧩 Key Features

✅ **AI-based DR classification** (ResNet152 / ResNet18)  
✅ **Modern dark-themed GUI** with gradient styling (Tkinter)  
✅ **Button hover effects** and neon animations  
✅ **Secure authentication** with SQLite-based user login/signup  
✅ **Real-time predictions** with detailed recommendations  
✅ **Integrated navigation** (upload, doctors directory, reviews, about)  
✅ **Offline operation** (no cloud dependency required)  
✅ **Review & feedback system** for quality improvement  

---

## 🧰 Technologies Used

| Category | Tools / Libraries |
|:----------|:----------------|
| **Deep Learning** | PyTorch, TorchVision |
| **GUI Development** | Tkinter, CustomTkinter |
| **Image Processing** | OpenCV, Pillow (PIL) |
| **Database** | SQLite |
| **Language** | Python 3.11+ |
| **IDE** | Visual Studio Code |
| **OS Tested** | Windows 10/11, Linux |

---

## 💎 Design Aesthetic

🎨 **Theme:** Deep midnight gradient (Black → Teal → Cyan)  
💡 **Font:** Segoe UI (bold, modern typography)  
✨ **Buttons:** Neon hover animation effects  
🧠 **Framework:** Native Tkinter – optimized for hospital environments  
🌙 **Mode:** Dark theme (eye-friendly for extended use)  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Adithyasivakumar/Team-Thiran-Diabetic-Retinopathy-Detection.git
cd Team-Thiran-Diabetic-Retinopathy-Detection
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```bash
python blindness.py
```

---

## 🎯 How to Use

### Step 1: Login / Sign Up
- **Default credentials** (for testing):
  - Username: `admin`
  - Password: `admin123`
- Create a new account for additional users

### Step 2: Upload Retinal Image
- Navigate to "Upload Report"
- Select a fundus image (`.jpg` or `.png` format)
- Click "Analyze" to get predictions

### Step 3: View Results
- AI model provides DR severity classification (0-4)
- Recommendations are displayed based on severity
- Review results and contact doctors if needed

### Step 4: Explore Features
- **Doctors Directory:** View ophthalmologist contacts in Tamil Nadu
- **Review Page:** Leave feedback on predictions and experience
- **About Page:** Learn more about the project and team

---

## 🔬 Model Architecture

| Component | Details |
|:-----------|:---------|
| **Base Model** | ResNet152 (PyTorch pretrained on ImageNet) |
| **Input Size** | 224×224 pixels |
| **Output Layer** | 5 neurons (Softmax for 5 DR classes) |
| **Loss Function** | Negative Log-Likelihood Loss (NLLLoss) |
| **Optimizer** | Adam (learning rate = 1e-5) |
| **Batch Size** | 32 (configurable) |
| **Validation Accuracy** | ≈ 85.6% |
| **Training Duration** | 2–5 epochs (CPU optimized) |

---

## 🧪 Dataset

📂 **Dataset Source:** [APTOS 2019 Blindness Detection (Kaggle)](https://www.kaggle.com/competitions/aptos2019-blindness-detection/data)

- **Total Images:** 3,662 labeled fundus images
- **Distribution:** Balanced across 5 DR severity classes (0-4)
- **Preprocessing:** Resize to 224×224, normalization, and augmentation applied
- **Train/Test Split:** 80% training, 20% validation

---

## 📁 Project Structure

```
Team-Thiran-Diabetic-Retinopathy-Detection/
├── blindness.py                    # Main GUI application
├── model.py                        # Model architecture definition
├── train_model.py                  # Model training script
├── inference.ipynb                 # Inference notebook
├── prepare_data.py                 # Data preprocessing
├── requirements.txt                # Python dependencies
├── dr_users.db                     # SQLite database (user data)
├── sampleimages/                   # Sample retinal images
├── images/                         # UI assets and screenshots
└── README.md                       # This file
```

---

## 🏥 Reference Ophthalmology Contacts (Tamil Nadu)

*Contacts provided for legitimate clinical awareness and patient follow-up only.*

| Hospital | Location | Contact |
|:---------|:---------|:--------|
| Aravind Eye Hospital | Madurai | +91 452 435 6100 |
| Sankara Nethralaya | Chennai | +91 44 4227 1500 |
| Dr. Agarwal's Eye Hospital | Coimbatore | +91 422 4411 111 |
| Lotus Eye Hospital | Salem | +91 427 2770 777 |
| Vasan Eye Care | Trichy | +91 431 241 4444 |

---

## 💬 Review & Feedback Page

Patients and users can:
- Rate the accuracy of AI predictions
- Leave feedback on interface usability
- Comment on doctor recommendations
- Track their diagnostic history

All reviews are stored securely in the local SQLite database for quality improvement and research purposes.

---

## 🌟 Future Enhancements

🔹 **Web Version** – Flask or Streamlit-based web interface  
🔹 **Explainable AI (XAI)** – Heatmaps for lesion visualization  
🔹 **Multi-language Support** – English & Tamil GUI  
🔹 **Federated Learning** – Privacy-focused distributed AI  
🔹 **Hospital Integration** – Connect with HMS (Hospital Management Systems)  
🔹 **Mobile App** – iOS/Android application for telemedicine  
🔹 **Real-time Monitoring** – Progress tracking for diabetic patients  

---

## 👨‍💻 Team

### 🔹 Team Lead
**Adithya S**
- Role: System Architecture, AI Workflow Planning, Project Coordination
- Contact: adithya07@gmail.com

### 🔹 Core Contributors
**Nhowmitha S**
- Role: GUI Design, Preprocessing Pipeline, Model Integration, Evaluation

**Melkin S**
- Role: AI Module Development, Dataset Preparation, Model Training, Performance Analysis

### 🔹 Key Contributor
**Bhavadharini G**
- Role: Application Workflow Design, UI/UX Support, Testing & Documentation

### 🔹 Mentor
**Mr. DL Mathew Valan**
- Role: Technical Guidance, System Validation, Project Review

---

## 💖 Acknowledgments

Special thanks to:

- **Aravind Eye Hospital, Madurai** – for inspiring this research vision and providing clinical insights
- **APTOS (Asia Pacific Tele-Ophthalmology Society)** – for open datasets and promoting global eye health awareness
- **Kaggle Community** – for hosting the APTOS 2019 dataset and benchmarking challenges

---

## 📝 License

This project is open-source and available under the MIT License.

---

## 🩶 Quote

> **"Empowering Vision Through Intelligence."** 👁️

---

<div align="center">

### 💫 If you found this project inspiring, give it a ⭐ on GitHub!
### Together, let's advance AI in healthcare. 🧠💙

</div>
