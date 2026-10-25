"""
DraftMate AI: Legal Drafting Studio Launcher
Run this script to start the studio backend and frontend interface.
Usage:
    python run.py
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*70)
    print("  ⚖️  DraftMate AI: Legal Drafting Studio (Kodekurrent Season 2)")
    print("  🌐  Frontend & API running at: http://127.0.0.1:8000")
    print("  📖  Interactive Swagger Docs: http://127.0.0.1:8000/docs")
    print("="*70 + "\n")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=[str(BASE_DIR)])
