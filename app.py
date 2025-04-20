from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

notes = []

@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()

    if not data or 'title' not in data or not data['title'].strip():
        return jsonify({'error': 'Title is required'}), 400

    new_note = {
        'id': len(notes) + 1,
        'title': data['title'],
        'content': data.get('content', ''),
        'created_at': request.date if hasattr(request, 'date') else None
    }

    notes.append(new_note)
    return jsonify({'message': 'Note created successfully', 'note': new_note}), 201

@app.route('/notes', methods=['GET'])
def list_notes():
    return jsonify({'notes': notes}), 200

@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json()

    # Find the note by ID
    note = next((note for note in notes if note['id'] == note_id), None)

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    # Validate title if present
    if 'title' in data and not data['title'].strip():
        return jsonify({'error': 'Title cannot be empty'}), 400

    # Update fields if provided
    note['title'] = data.get('title', note['title'])
    note['content'] = data.get('content', note['content'])

    return jsonify({'message': 'Note updated successfully', 'note': note}), 200

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    global notes
    note = next((note for note in notes if note['id'] == note_id), None)

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    notes = [note for note in notes if note['id'] != note_id]
    return jsonify({'message': 'Note deleted successfully'}), 200

@app.route('/notes/search', methods=['GET'])
def search_notes():
    query = request.args.get('q', '').strip().lower()

    if not query:
        return jsonify({'error': 'Search keyword or ID is required'}), 400

    # Try searching by note ID
    if query.isdigit():
        note_id = int(query)
        note = next((note for note in notes if note['id'] == note_id), None)
        if note:
            return jsonify({'results': [note]}), 200

    # Fallback: search by keyword in title/content
    filtered_notes = [
        note for note in notes
        if query in note['title'].lower() or query in note['content'].lower()
    ]

    return jsonify({'results': filtered_notes}), 200


if __name__ == '__main__':
    app.run(debug=True)
