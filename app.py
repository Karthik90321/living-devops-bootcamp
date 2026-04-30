# Import the Flask class from the flask library
# Flask is a lightweight web framework for Python
from flask import Flask

# Create an instance of the Flask application
# __name__ tells Flask where to look for resources (templates, static files, etc.)
app = Flask(__name__)

# Define a route for the root URL "/"
# When someone visits http://your-server:5000/ , this function runs
@app.route('/')
def home():
    # Return a plain text response to the browser
    return "DevOps Project is Running 🚀"

# Define a route for "/health"
# Health check endpoints are standard in DevOps — used by load balancers (like AWS ALB)
# and container orchestrators (like ECS/Kubernetes) to verify the app is alive
@app.route('/health')
def health():
    # Returning a Python dict — Flask automatically converts it to a JSON response
    # e.g., {"status": "healthy"} with Content-Type: application/json
    return {"status": "healthy"}

# Python entry point guard
# This block only runs when you execute the file directly: python app.py
# It does NOT run if this file is imported as a module by another script
if __name__ == '__main__':
    # Start the Flask development server with these settings:
    # host='0.0.0.0' → listen on ALL network interfaces (not just localhost)
    #                   This is essential inside Docker containers or EC2
    #                   so external traffic can reach the app
    # port=5000       → serve on port 5000
    app.run(host='0.0.0.0', port=5000)