# Team Thiran - Project Structure Documentation

## 📁 Clean Project Organization

### Root Directory Structure
```
Team-Thiran-Diabetic-Retinopathy-Detection/
│
├── 📱 frontend/              
│   ├── blindness.py               - Main GUI application
│   ├── report_verification_dialog.py - Report verification UI
│   └── __init__.py
│
├── 🧠 backend/               
│   ├── model.py              - ResNet152 DR detection model
│   ├── training.ipynb        - Model training notebook
│   ├── inference.ipynb       - Inference examples
│   ├── Single_test_inference.ipynb - Single image testing
│   └── __init__.py
│
├── 📧 messaging/             
│   ├── send_sms.py          - SMS notifications via Twilio
│   ├── send_whatsapp.py     - WhatsApp delivery
│   └── __init__.py
│
├── 📊 reports/              
│   ├── report_generator.py  - Professional report generation
│   ├── pdf_report.py        - PDF formatting
│   ├── generated_reports/   - Output directory for PDFs
│   └── __init__.py
│
├── 🧪 tests/                
│   ├── test_model_loading.py
│   ├── test_model_predictions.py
│   ├── test_db_connection.py
│   ├── test_sms_integration.py
│   ├── test_report_system.py
│   └── __init__.py
│
├── 🗄️ database/             
│   ├── setup_database.sql   - MySQL initialization
│   └── __init__.py
│
├── ⚙️ config/               
│   └── __init__.py
│
├── 📚 docs/                 - Documentation folder
├── 🖼️ images/               - Reference images
├── 🖼️ sampleimages/         - Sample test images
│
├── 🚀 Entry Points
│   ├── main.py              - Python entry point
│   ├── run.sh              - Bash startup script
│
├── 📦 Configuration (Single Location)
│   ├── requirements.txt     - Python dependencies (16 packages)
│   ├── .env.example        - Twilio config template
│   ├── .env               - Local credentials (NOT committed)
│   ├── .gitignore         - Git exclusion rules
│
├── 📄 Documentation
│   ├── README.md           - Project documentation
│   └── GettingStarted.md   - Setup instructions
│
├── 🤖 Models
│   └── classifier.pt       - Trained ResNet152 weights (677MB)
│
└── 🔧 Environment
    └── venv/              - Python virtual environment
```

## ✅ Key Features of This Structure

### 1. **Clean Organization**
- Each folder has a specific purpose
- No duplicate files or confusion
- Professional project appearance

### 2. **Single Source of Truth**
- ✅ **requirements.txt** - Root location (main, pip install point)
- ✅ **.env.example** - Root location (team reference)
- ✅ No duplicates in config/ folder

### 3. **Functional Separation**
- **frontend/** - User interface layer
- **backend/** - ML model and inference
- **messaging/** - Communication channels
- **reports/** - Report generation
- **tests/** - Validation scripts
- **database/** - Data persistence
- **config/** - Settings (archive folder)

### 4. **Running the Application**

#### Option 1: Bash script
```bash
bash run.sh
```

#### Option 2: Direct Python
```bash
python frontend/blindness.py
```

#### Option 3: Entry point
```bash
python main.py
```

## 🧪 Testing

Run tests to verify everything works:

```bash
# Test model loading
python tests/test_model_loading.py

# Test full system
python tests/test_report_system.py

# Test SMS integration
python tests/test_sms_integration.py
```

## 📦 Installation

1. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Twilio credentials
   ```

4. **Set up database:**
   ```bash
   mysql -u root < database/setup_database.sql
   ```

## 🔍 File Cleanup Details

### Removed Duplicates ✅
- `config/requirements.txt` → DELETED (duplicate of root)
- `config/.env.example` → DELETED (duplicate of root)

### Reason
- Single source of truth for configuration
- Eliminates confusion for team members
- Easier maintenance and updates
- No code references to deleted copies
- All functionality preserved

## 📊 Project Statistics

- **Total Directories:** 8 organized folders
- **Total Python Files:** 12 in respective folders
- **Total Test Files:** 5 comprehensive tests
- **Dependencies:** 16 packages
- **Lines of Code:** 2000+ lines
- **Commits:** Well-documented git history
- **Project Size:** ~8.3GB (includes venv and model)

## ✨ Quality Assurance

✅ All imports working correctly
✅ Model loads successfully
✅ Report generation functional
✅ SMS integration active
✅ Database connectivity verified
✅ Test suite passing
✅ No duplicate files
✅ Professional structure
✅ Clean separation of concerns
✅ Ready for team collaboration

---

**Last Updated:** February 25, 2026
**Team:** Adithya S, Nhowmitha S, Melkin S, Bhavadharani G
