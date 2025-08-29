from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directories
os.makedirs('uploads/photos', exist_ok=True)
os.makedirs('uploads/music', exist_ok=True)
os.makedirs('uploads/artwork', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Data storage files
MESSAGES_FILE = 'data/messages.json'
GALLERY_FILE = 'data/gallery.json'

def load_json_file(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return render_template('birthday.html')  # Your HTML file

@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo uploaded'}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join('uploads/photos', unique_filename)
        
        file.save(file_path)
        
        # Save to gallery data
        gallery = load_json_file(GALLERY_FILE)
        photo_data = {
            'id': str(uuid.uuid4()),
            'filename': unique_filename,
            'original_name': file.filename,
            'upload_date': datetime.now().isoformat(),
            'url': f'/uploads/photos/{unique_filename}'
        }
        gallery.append(photo_data)
        save_json_file(GALLERY_FILE, gallery)
        
        return jsonify({
            'success': True,
            'photo': photo_data
        })

@app.route('/gallery')
def get_gallery():
    gallery = load_json_file(GALLERY_FILE)
    return jsonify(gallery)

@app.route('/delete-photo/<photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    gallery = load_json_file(GALLERY_FILE)
    photo_to_delete = None
    
    for i, photo in enumerate(gallery):
        if photo['id'] == photo_id:
            photo_to_delete = gallery.pop(i)
            break
    
    if photo_to_delete:
        # Delete file from disk
        file_path = os.path.join('uploads/photos', photo_to_delete['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)
        
        save_json_file(GALLERY_FILE, gallery)
        return jsonify({'success': True})
    
    return jsonify({'error': 'Photo not found'}), 404

@app.route('/save-message', methods=['POST'])
def save_message():
    data = request.get_json()
    message_text = data.get('message', '').strip()
    
    if not message_text:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    messages = load_json_file(MESSAGES_FILE)
    new_message = {
        'id': str(uuid.uuid4()),
        'message': message_text,
        'timestamp': datetime.now().isoformat(),
        'date_display': datetime.now().strftime('%B %d, %Y at %I:%M %p')
    }
    
    messages.append(new_message)
    save_json_file(MESSAGES_FILE, messages)
    
    return jsonify({
        'success': True,
        'message': new_message
    })

@app.route('/messages')
def get_messages():
    messages = load_json_file(MESSAGES_FILE)
    return jsonify(messages)

@app.route('/delete-message/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    messages = load_json_file(MESSAGES_FILE)
    
    for i, message in enumerate(messages):
        if message['id'] == message_id:
            messages.pop(i)
            save_json_file(MESSAGES_FILE, messages)
            return jsonify({'success': True})
    
    return jsonify({'error': 'Message not found'}), 404

@app.route('/save-artwork', methods=['POST'])
def save_artwork():
    data = request.get_json()
    artwork_data = data.get('artwork')
    
    if not artwork_data:
        return jsonify({'error': 'No artwork data provided'}), 400
    
    # Save artwork as base64 data
    unique_filename = f"artwork_{uuid.uuid4()}.json"
    artwork_info = {
        'id': str(uuid.uuid4()),
        'filename': unique_filename,
        'created_date': datetime.now().isoformat(),
        'data': artwork_data
    }
    
    file_path = os.path.join('uploads/artwork', unique_filename)
    with open(file_path, 'w') as f:
        json.dump(artwork_info, f)
    
    return jsonify({
        'success': True,
        'artwork': artwork_info
    })

@app.route('/upload-music', methods=['POST'])
def upload_music():
    if 'music' not in request.files:
        return jsonify({'error': 'No music file uploaded'}), 400
    
    file = request.files['music']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is audio
    allowed_extensions = {'mp3', 'wav', 'ogg', 'm4a', 'aac'}
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    
    if file_extension not in allowed_extensions:
        return jsonify({'error': 'Invalid audio file format'}), 400
    
    if file:
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join('uploads/music', unique_filename)
        file.save(file_path)
        
        return jsonify({
            'success': True,
            'music': {
                'filename': unique_filename,
                'original_name': file.filename,
                'url': f'/uploads/music/{unique_filename}'
            }
        })

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploads/photos/<filename>')
def uploaded_photo(filename):
    return send_from_directory('uploads/photos', filename)

@app.route('/uploads/music/<filename>')
def uploaded_music(filename):
    return send_from_directory('uploads/music', filename)

@app.route('/uploads/artwork/<filename>')
def uploaded_artwork(filename):
    return send_from_directory('uploads/artwork', filename)

# Birthday countdown API
@app.route('/api/countdown')
def countdown_api():
    # You can customize the birthday date here
    birthday_date = "2025-09-03"
    return jsonify({
        'birthday_date': birthday_date,
        'message': 'Countdown to Nipa\'s Birthday!'
    })

# Health check
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)