#!/usr/bin/env python3
"""
Team Thiran - Diabetic Retinopathy Detection System
Main entry point for the GUI application

To run this application:
    python main.py
    OR
    python frontend/blindness.py
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == '__main__':
    print("=" * 60)
    print("Team Thiran - Diabetic Retinopathy Detection System")
    print("=" * 60)
    print("Starting GUI application...")
    print()
    
    # Import and run the frontend application
    try:
        from frontend import blindness
        # The blindness module will handle running the GUI via if __name__ == '__main__'
        # This will only execute if blindness.py is run directly
        print("GUI application initialized.")
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
