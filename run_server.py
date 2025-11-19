#!/usr/bin/env python3
"""
Run Flask server without debug mode for testing
"""
from app import app

if __name__ == '__main__':
    # Run without debug mode to avoid terminal issues
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
