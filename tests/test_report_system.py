#!/usr/bin/env python3
"""
Test Report Generation System
Verifies all components work correctly
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_report_generation():
    """Test medical report generation"""
    print("\n" + "="*60)
    print("Testing Report Generation System")
    print("="*60)
    
    # Test 1: Report Generator
    print("\n1. Testing Report Generation Module...")
    try:
        from reports.report_generator import create_report, MedicalReportGenerator
        
        report = create_report(
            username="test_patient",
            severity_level=2,
            confidence_score=85.5,
            image_path="/path/to/image.jpg",
            age=45,
            gender="Male"
        )
        
        print("   ✅ Report generated successfully")
        print(f"   Report ID: {report['report_id']}")
        print(f"   Classification: {report['findings']['classification']}")
        print(f"   Risk Level: {report['findings']['risk_level']}")
        
    except Exception as e:
        print(f"   ❌ Report generation failed: {e}")
        return False
    
    # Test 2: PDF Generation
    print("\n2. Testing PDF Report Generation...")
    try:
        from reports.pdf_report import create_pdf_report
        
        pdf_path = create_pdf_report(report, image_path=None)
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path) / 1024  # KB
            print(f"   ✅ PDF created successfully")
            print(f"   File: {pdf_path}")
            print(f"   Size: {file_size:.1f} KB")
        else:
            print(f"   ❌ PDF file not found")
            return False
            
    except Exception as e:
        print(f"   ❌ PDF generation failed: {e}")
        return False
    
    # Test 3: Report Summary Functions
    print("\n3. Testing Report Summary Functions...")
    try:
        generator = MedicalReportGenerator("test_patient", "test_patient", 45, "Male")
        
        sms_summary = generator.get_report_summary(report)
        print(f"   ✅ SMS Summary generated ({len(sms_summary)} chars)")
        
        whatsapp_text = generator.get_report_text(report)
        print(f"   ✅ WhatsApp text generated ({len(whatsapp_text)} chars)")
        
    except Exception as e:
        print(f"   ❌ Summary generation failed: {e}")
        return False
    
    # Test 4: Verification Dialog Import
    print("\n4. Testing Report Verification Dialog...")
    try:
        from frontend.report_verification_dialog import show_verification_dialog
        print("   ✅ Verification dialog module imported successfully")
        
    except Exception as e:
        print(f"   ❌ Dialog import failed: {e}")
        return False
    
    # Test 5: Send Modules
    print("\n5. Testing Send Modules (Import Only)...")
    try:
        from messaging.send_sms import send_report_sms
        from messaging.send_whatsapp import send_report_whatsapp
        
        print("   ✅ SMS module imported successfully")
        print("   ✅ WhatsApp module imported successfully")
        
    except Exception as e:
        print(f"   ❌ Send module import failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\nProject Structure:")
    print("  - report_generator.py ................. Medical report generation")
    print("  - pdf_report.py ....................... PDF creation")
    print("  - report_verification_dialog.py ...... User verification UI")
    print("  - send_sms.py ......................... SMS with report support")
    print("  - send_whatsapp.py ................... WhatsApp with PDF")
    print("  - blindness.py ........................ Updated with new workflow")
    print("\nWorkflow:")
    print("  1. User uploads retinal image")
    print("  2. Model predicts DR classification")
    print("  3. System generates medical report")
    print("  4. PDF created with professional formatting")
    print("  5. Verification dialog shows report (user reviews)")
    print("  6. User selects delivery method (SMS/WhatsApp/Both)")
    print("  7. Report sent to patient via selected channel(s)")
    print("\nGenerated reports stored in: reports/ directory")
    print("="*60 + "\n")
    
    return True

if __name__ == '__main__':
    success = test_report_generation()
    sys.exit(0 if success else 1)
