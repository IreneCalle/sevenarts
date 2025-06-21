from app import app
from scheduler import start_scheduler
import logging

if __name__ == '__main__':
    # Start the scheduler
    start_scheduler()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
