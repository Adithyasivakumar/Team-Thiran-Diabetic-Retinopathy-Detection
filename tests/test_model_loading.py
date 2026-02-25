import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try to load the model and report any issues
try:
    from backend.model import model
    print("✅ SUCCESS: Model loaded successfully!")
    print(f"Model type: {type(model)}")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
