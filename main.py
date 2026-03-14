import os
from flask import Flask, request, jsonify
from google.cloud import firestore

# Initialize Flask app
app = Flask(_name_)

# Initialize Firestore Client
# It will automatically use the project ID from the environment
db = firestore.Client()

@app.route('/', methods=['GET'])
def home():
    """
    Root endpoint to handle base URL requests.
    This prevents the 404 error you were seeing.
    """
    return jsonify({
        "message": "Welcome to the Notes API!",
        "status": "Running",
        "endpoints": {
            "health": "/health",
            "get_notes": "/notes (GET)",
            "add_note": "/notes (POST)"
        }
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@app.route('/notes', methods=['GET'])
def get_notes():
    """Fetch all documents from the 'notes' collection."""
    try:
        notes_ref = db.collection('notes')
        # streaming the results into a list of dictionaries
        notes = [doc.to_dict() for doc in notes_ref.stream()]
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/notes', methods=['POST'])
def add_note():
    """Add a new note sent as JSON in the request body."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Add to Firestore
        db.collection('notes').add(data)
        return jsonify({"success": True, "message": "Note added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name_ == "__main__":
    # Cloud Run passes the port to use in the PORT environment variable.
    # We default to 8080 for local testing.
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
