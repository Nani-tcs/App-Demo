import os
from flask import Flask, request, jsonify
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/notes', methods=['GET'])
def get_notes():
    notes = [doc.to_dict() for doc in db.collection('notes').stream()]
    return jsonify(notes), 200

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.json
    db.collection('notes').add(data)
    return jsonify({"success": True}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
