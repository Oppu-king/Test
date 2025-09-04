from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get configuration from environment variables
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('FLASK_ENV') != 'production'

if not OPENROUTER_API_KEY:
    print("⚠️ Warning: OPENROUTER_API_KEY environment variable not set!")

@app.route('/')
def index():
    """Serve the main Nipa website"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """Handle AI chat requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        system_prompt = data.get('system_prompt', 
            "You are Nipa, a helpful AI assistant for girls. You're friendly, supportive, and knowledgeable about fashion, beauty, wellness, and lifestyle. Always respond in a girly, encouraging tone with emojis.")
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        ai_response = call_openrouter_api(message, system_prompt)
        return jsonify({'response': ai_response})
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/fashion/outfit', methods=['POST'])
def generate_outfit():
    """Generate outfit recommendations"""
    try:
        data = request.get_json()
        occasion = data.get('occasion', '')
        weather = data.get('weather', '')
        style = data.get('style', '')
        
        if not all([occasion, weather, style]):
            return jsonify({'error': 'All fields are required'}), 400
        
        prompt = f"Create a detailed outfit recommendation for a {style} style, {occasion} occasion, in {weather} weather. Include specific clothing items, colors, accessories, and styling tips. Make it girly and fashionable!"
        
        system_prompt = "You are a professional fashion stylist AI. Provide detailed, practical outfit recommendations with specific items, colors, and styling tips. Be enthusiastic and use emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        return jsonify({'outfit': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/beauty/skincare', methods=['POST'])
def generate_skincare_routine():
    """Generate personalized skincare routine"""
    try:
        data = request.get_json()
        skin_type = data.get('skin_type', '')
        concerns = data.get('concerns', '')
        budget = data.get('budget', '')
        
        if not all([skin_type, concerns, budget]):
            return jsonify({'error': 'All fields are required'}), 400
        
        prompt = f"Create a personalized skincare routine for {skin_type} skin with {concerns} concerns, within a {budget} budget. Include morning and evening routines, specific product recommendations, and application tips."
        
        system_prompt = "You are a skincare expert AI. Provide detailed, personalized skincare routines with specific product recommendations, application order, and helpful tips. Be encouraging and use emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        return jsonify({'routine': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/wellness/cycle', methods=['POST'])
def calculate_cycle():
    """Calculate menstrual cycle predictions"""
    try:
        data = request.get_json()
        last_period = data.get('last_period', '')
        cycle_length = int(data.get('cycle_length', 28))
        
        if not last_period:
            return jsonify({'error': 'Last period date is required'}), 400
        
        # Parse date
        last_period_date = datetime.strptime(last_period, '%Y-%m-%d')
        
        # Calculate predictions
        next_period = last_period_date + timedelta(days=cycle_length)
        ovulation = last_period_date + timedelta(days=cycle_length // 2)
        fertile_start = ovulation - timedelta(days=5)
        fertile_end = ovulation + timedelta(days=1)
        
        return jsonify({
            'next_period': next_period.strftime('%Y-%m-%d'),
            'ovulation': ovulation.strftime('%Y-%m-%d'),
            'fertile_start': fertile_start.strftime('%Y-%m-%d'),
            'fertile_end': fertile_end.strftime('%Y-%m-%d')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/wellness/workout', methods=['POST'])
def generate_workout_plan():
    """Generate personalized workout plan"""
    try:
        data = request.get_json()
        goal = data.get('goal', '')
        time = data.get('time', '')
        
        if not all([goal, time]):
            return jsonify({'error': 'All fields are required'}), 400
        
        prompt = f"Create a {time}-minute daily workout plan for {goal}. Include specific exercises, sets, reps, and modifications for beginners. Make it female-focused and motivating!"
        
        system_prompt = "You are a fitness trainer AI specializing in women's fitness. Provide detailed, safe, and effective workout plans with clear instructions and motivational language. Use emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        return jsonify({'workout': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lifestyle/mood', methods=['POST'])
def handle_mood():
    """Handle mood tracking and response"""
    try:
        data = request.get_json()
        mood = data.get('mood', '')
        emoji = data.get('emoji', '')
        
        if not mood:
            return jsonify({'error': 'Mood is required'}), 400
        
        prompt = f"The user is feeling {mood} today {emoji}. Provide a supportive, encouraging response with personalized advice, self-care tips, or activities that match their mood. Keep it girly and uplifting!"
        
        system_prompt = "You are a supportive friend AI. Provide empathetic, encouraging responses with practical self-care advice based on the user's mood. Be warm, understanding, and use emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lifestyle/affirmation', methods=['GET'])
def generate_affirmation():
    """Generate daily affirmation"""
    try:
        prompt = "Generate a powerful, personalized daily affirmation for a girl to boost her confidence, self-love, and motivation. Make it empowering and beautiful!"
        
        system_prompt = "You are a motivational coach AI. Create inspiring, personalized affirmations that boost confidence and self-love. Be empowering and use beautiful language with emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        return jsonify({'affirmation': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lifestyle/selfcare', methods=['POST'])
def generate_selfcare():
    """Generate self-care routine"""
    try:
        data = request.get_json()
        time = data.get('time', '')
        
        if not time:
            return jsonify({'error': 'Time is required'}), 400
        
        prompt = f"Create a personalized {time}-minute self-care routine. Include specific activities, products to use, and steps to follow. Make it relaxing and rejuvenating!"
        
        system_prompt = "You are a self-care expert AI. Provide detailed, relaxing self-care routines with specific activities and steps. Be soothing and encouraging with emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        return jsonify({'routine': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shopping/products', methods=['POST'])
def find_products():
    """Find product recommendations"""
    try:
        data = request.get_json()
        category = data.get('category', '')
        budget = data.get('budget', '')
        specific = data.get('specific', '')
        
        if not all([category, budget]):
            return jsonify({'error': 'Category and budget are required'}), 400
        
        prompt = f"Find the best {category} products within {budget} budget{' specifically for \"' + specific + '\"' if specific else ''}. Include product names, price ranges, where to buy, and why they're great. Focus on quality and value!"
        
        system_prompt = "You are a shopping expert AI. Provide detailed product recommendations with prices, where to buy, and honest reviews. Be helpful and enthusiastic with emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        return jsonify({'products': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/community/question', methods=['POST'])
def handle_anonymous_question():
    """Handle anonymous community questions"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        prompt = f"Answer this anonymous question from a girl: \"{question}\". Provide supportive, non-judgmental advice with empathy and understanding. Be like a caring big sister!"
        
        system_prompt = "You are a supportive community moderator AI. Provide caring, non-judgmental advice to anonymous questions. Be empathetic, understanding, and like a caring big sister with emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/community/girl-talk', methods=['GET'])
def generate_girl_talk_topic():
    """Generate girl talk discussion topic"""
    try:
        prompt = "Generate an engaging, fun discussion topic for girls to chat about. It could be about relationships, fashion, beauty, life experiences, or personal growth. Make it thought-provoking but light-hearted!"
        
        system_prompt = "You are a community engagement AI. Create fun, engaging discussion topics that girls would love to chat about. Be creative and inclusive with emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        return jsonify({'topic': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/community/style-challenge', methods=['GET'])
def generate_style_challenge():
    """Generate weekly style challenge"""
    try:
        prompt = "Create a fun, creative weekly style challenge for girls. Include specific goals, styling tips, and ways to participate. Make it inclusive and encouraging for all body types and budgets!"
        
        system_prompt = "You are a style challenge creator AI. Design fun, inclusive fashion challenges that encourage creativity and self-expression. Be motivating and use emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        return jsonify({'challenge': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def call_openrouter_api(prompt, system_prompt):
    """Helper function to call OpenRouter API"""
    try:
        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            'model': 'deepseek/deepseek-chat',
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 500
        }
        
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Sorry babe! I'm having trouble connecting right now. Please try again in a moment! 💕 (Error: {response.status_code})"
            
    except Exception as e:
        return f"Sorry babe! I'm having trouble connecting right now. Please try again in a moment! 💕 (Error: {str(e)})"

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if API key is set
    if not OPENROUTER_API_KEY:
        print("⚠️ Warning: Please set the OPENROUTER_API_KEY environment variable!")
        print("Example: export OPENROUTER_API_KEY='your-api-key-here'")
    else:
        print("✅ OpenRouter API key loaded successfully!")
    
    print("🌺 Starting Nipa server...")
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)