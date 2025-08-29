from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nipa-birthday-secret-key-2024'
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
ARTWORK_FILE = 'data/artwork.json'
MUSIC_FILE = 'data/music.json'

def load_json_file(filename, default=None):
    """Load JSON data from file with error handling"""
    if default is None:
        default = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json_file(filename, data):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

# ==================== MAIN ROUTES ====================

@app.route('/')
def home():
    """Main birthday website page"""
    return render_template('birthday.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Nipa\'s Birthday Website is running!'
    })

# ==================== ENHANCED PHOTO GALLERY ROUTES ====================

@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    """Upload photo to gallery with enhanced features"""
    try:
        if 'photo' not in request.files:
            return jsonify({'error': 'No photo uploaded'}), 400
        
        file = request.files['photo']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
        if not allowed_file(file.filename, allowed_extensions):
            return jsonify({'error': 'Invalid image format. Allowed: PNG, JPG, JPEG, GIF, WEBP, BMP'}), 400
        
        # Generate secure filename
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join('uploads/photos', unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Save to gallery data with enhanced metadata
        gallery = load_json_file(GALLERY_FILE)
        photo_data = {
            'id': str(uuid.uuid4()),
            'filename': unique_filename,
            'original_name': original_filename,
            'upload_date': datetime.now().isoformat(),
            'display_date': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
            'url': f'/uploads/photos/{unique_filename}',
            'size': os.path.getsize(file_path),
            'views': 0,
            'likes': 0
        }
        gallery.append(photo_data)
        save_json_file(GALLERY_FILE, gallery)
        
        return jsonify({
            'success': True,
            'message': 'Photo uploaded successfully!',
            'photo': photo_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/gallery')
def get_gallery():
    """Get all photos in gallery with stats"""
    gallery = load_json_file(GALLERY_FILE)
    # Sort by upload date, newest first
    gallery.sort(key=lambda x: x.get('upload_date', ''), reverse=True)
    
    return jsonify({
        'success': True,
        'photos': gallery,
        'count': len(gallery),
        'total_size': sum(photo.get('size', 0) for photo in gallery),
        'total_views': sum(photo.get('views', 0) for photo in gallery)
    })

@app.route('/delete-photo/<photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    """Delete photo from gallery"""
    try:
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
            return jsonify({
                'success': True,
                'message': 'Photo deleted successfully!'
            })
        
        return jsonify({'error': 'Photo not found'}), 404
        
    except Exception as e:
        return jsonify({'error': f'Delete failed: {str(e)}'}), 500

@app.route('/like-photo/<photo_id>', methods=['POST'])
def like_photo(photo_id):
    """Like a photo"""
    try:
        gallery = load_json_file(GALLERY_FILE)
        
        for photo in gallery:
            if photo['id'] == photo_id:
                photo['likes'] = photo.get('likes', 0) + 1
                save_json_file(GALLERY_FILE, gallery)
                return jsonify({
                    'success': True,
                    'likes': photo['likes']
                })
        
        return jsonify({'error': 'Photo not found'}), 404
        
    except Exception as e:
        return jsonify({'error': f'Like failed: {str(e)}'}), 500

# ==================== ENHANCED MESSAGES ROUTES ====================

@app.route('/save-message', methods=['POST'])
def save_message():
    """Save birthday message with enhanced features"""
    try:
        data = request.get_json()
        message_text = data.get('message', '').strip()
        author = data.get('author', 'Anonymous').strip()
        
        if not message_text:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        messages = load_json_file(MESSAGES_FILE)
        new_message = {
            'id': str(uuid.uuid4()),
            'message': message_text,
            'author': author,
            'timestamp': datetime.now().isoformat(),
            'date_display': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
            'likes': 0,
            'is_wish': data.get('is_wish', False)
        }
        
        messages.append(new_message)
        save_json_file(MESSAGES_FILE, messages)
        
        return jsonify({
            'success': True,
            'message': 'Message saved successfully!',
            'data': new_message
        })
        
    except Exception as e:
        return jsonify({'error': f'Save failed: {str(e)}'}), 500

@app.route('/messages')
def get_messages():
    """Get all birthday messages"""
    messages = load_json_file(MESSAGES_FILE)
    # Sort by timestamp, newest first
    messages.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return jsonify({
        'success': True,
        'messages': messages,
        'count': len(messages),
        'total_likes': sum(msg.get('likes', 0) for msg in messages)
    })

@app.route('/like-message/<message_id>', methods=['POST'])
def like_message(message_id):
    """Like a birthday message"""
    try:
        messages = load_json_file(MESSAGES_FILE)
        
        for message in messages:
            if message['id'] == message_id:
                message['likes'] = message.get('likes', 0) + 1
                save_json_file(MESSAGES_FILE, messages)
                return jsonify({
                    'success': True,
                    'likes': message['likes']
                })
        
        return jsonify({'error': 'Message not found'}), 404
        
    except Exception as e:
        return jsonify({'error': f'Like failed: {str(e)}'}), 500

# ==================== ENHANCED ARTWORK ROUTES ====================

@app.route('/save-artwork', methods=['POST'])
def save_artwork():
    """Save digital artwork with metadata"""
    try:
        data = request.get_json()
        artwork_data = data.get('artwork')
        title = data.get('title', 'Untitled Artwork')
        
        if not artwork_data:
            return jsonify({'error': 'No artwork data provided'}), 400
        
        # Save artwork
        artworks = load_json_file(ARTWORK_FILE)
        artwork_info = {
            'id': str(uuid.uuid4()),
            'title': title,
            'created_date': datetime.now().isoformat(),
            'display_date': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
            'data': artwork_data,
            'likes': 0,
            'views': 0
        }
        
        artworks.append(artwork_info)
        save_json_file(ARTWORK_FILE, artworks)
        
        return jsonify({
            'success': True,
            'message': 'Artwork saved successfully!',
            'artwork': artwork_info
        })
        
    except Exception as e:
        return jsonify({'error': f'Save failed: {str(e)}'}), 500

@app.route('/artworks')
def get_artworks():
    """Get all saved artworks"""
    artworks = load_json_file(ARTWORK_FILE)
    # Sort by creation date, newest first
    artworks.sort(key=lambda x: x.get('created_date', ''), reverse=True)
    return jsonify({
        'success': True,
        'artworks': artworks,
        'count': len(artworks)
    })

# ==================== ENHANCED MUSIC ROUTES ====================

@app.route('/upload-music', methods=['POST'])
def upload_music():
    """Upload music file with enhanced features"""
    try:
        if 'music' not in request.files:
            return jsonify({'error': 'No music file uploaded'}), 400
        
        file = request.files['music']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file type
        allowed_extensions = {'mp3', 'wav', 'ogg', 'm4a', 'aac', 'flac'}
        if not allowed_file(file.filename, allowed_extensions):
            return jsonify({'error': 'Invalid audio format. Allowed: MP3, WAV, OGG, M4A, AAC, FLAC'}), 400
        
        # Generate secure filename
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join('uploads/music', unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Save to music data
        music_files = load_json_file(MUSIC_FILE)
        music_data = {
            'id': str(uuid.uuid4()),
            'filename': unique_filename,
            'original_name': original_filename,
            'upload_date': datetime.now().isoformat(),
            'display_date': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
            'url': f'/uploads/music/{unique_filename}',
            'size': os.path.getsize(file_path),
            'plays': 0,
            'likes': 0
        }
        music_files.append(music_data)
        save_json_file(MUSIC_FILE, music_files)
        
        return jsonify({
            'success': True,
            'message': 'Music uploaded successfully!',
            'music': music_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/music')
def get_music():
    """Get all music files"""
    music_files = load_json_file(MUSIC_FILE)
    return jsonify({
        'success': True,
        'music': music_files,
        'count': len(music_files),
        'total_plays': sum(music.get('plays', 0) for music in music_files)
    })

# ==================== FILE SERVING ROUTES ====================

@app.route('/uploads/photos/<filename>')
def uploaded_photo(filename):
    """Serve uploaded photos"""
    return send_from_directory('uploads/photos', filename)

@app.route('/uploads/music/<filename>')
def uploaded_music(filename):
    """Serve uploaded music"""
    return send_from_directory('uploads/music', filename)

@app.route('/uploads/artwork/<filename>')
def uploaded_artwork(filename):
    """Serve uploaded artwork"""
    return send_from_directory('uploads/artwork', filename)

# ==================== API ROUTES ====================

@app.route('/api/stats')
def get_stats():
    """Get comprehensive website statistics"""
    try:
        gallery = load_json_file(GALLERY_FILE)
        messages = load_json_file(MESSAGES_FILE)
        artworks = load_json_file(ARTWORK_FILE)
        music_files = load_json_file(MUSIC_FILE)
        
        return jsonify({
            'success': True,
            'stats': {
                'total_photos': len(gallery),
                'total_messages': len(messages),
                'total_artworks': len(artworks),
                'total_music': len(music_files),
                'total_likes': sum(msg.get('likes', 0) for msg in messages) + 
                              sum(photo.get('likes', 0) for photo in gallery),
                'total_plays': sum(music.get('plays', 0) for music in music_files),
                'total_storage': sum(photo.get('size', 0) for photo in gallery) + 
                               sum(music.get('size', 0) for music in music_files),
                'last_updated': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Stats failed: {str(e)}'}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(413)
def too_large_error(error):
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    # Ensure directories exist
    for directory in ['uploads/photos', 'uploads/music', 'uploads/artwork', 'data']:
        os.makedirs(directory, exist_ok=True)
    
    # Initialize empty data files if they don't exist
    for file_path in [MESSAGES_FILE, GALLERY_FILE, ARTWORK_FILE, MUSIC_FILE]:
        if not os.path.exists(file_path):
            save_json_file(file_path, [])
    
    print("🎂 Starting Nipa's Enhanced Birthday Website...")
    print("📸 Photo Gallery: Multiple uploads, server storage ✅")
    print("💌 Messages System: Enhanced with likes ✅") 
    print("🎵 Music Player: Auto-play birthday song ✅")
    print("🎨 Art Studio: Server storage ✅")
    print("✨ All enhanced features ready!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)