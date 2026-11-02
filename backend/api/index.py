import sys
from pathlib import Path

# Add backend directory to sys.path so app modules import cleanly on Vercel
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from app.main import app
