import os
from flask import Flask, request, jsonify
from google.cloud import firestore

# Initialize Flask app
app = Flask(_name_)

# Initialize Firestore Client
# Cloud Run automatically picks up project credentials 
# if the Service Account has the correct roles.
db = firestore.Client()

@app.route('/', methods=['GET'])
def index():
    """Root endpoint to prevent 404 errors when visiting the base URL."""
    return jsonify({
        "message": "Welcome to the Notes API!",
        "status": "online",
        "endpoints": {
            "health_check": "/health",
            "list_notes": "/notes (GET)",
            "add_note": "/notes (POST)"
        }
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Basic health check for monitoring."""
    return jsonify({"status": "healthy"}), 200

@app.route('/notes', methods=['GET'])
def get_notes():
    """Retrieve all notes from the Firestore 'notes' collection."""
    try:
        notes_ref = db.collection('notes')
        notes = [doc.to_dict() for doc in notes_ref.stream()]
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/notes', methods=['POST'])
def add_note():
    """Add a new note to Firestore."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Adds a new document with an auto-generated ID
        db.collection('notes').add(data)
        return jsonify({"success": True, "message": "Note added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if _name_ == "_main_":
    # Cloud Run provides the PORT environment variable.
    # It defaults to 8080 if not set.
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
