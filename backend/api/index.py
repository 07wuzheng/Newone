"""Vercel serverless entry point using Mangum ASGI adapter."""
import os
import sys

# Ensure backend package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangum import Mangum
from main import app

handler = Mangum(app)
