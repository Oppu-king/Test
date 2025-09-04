from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json
from datetime import datetime, timedelta
from flask import render_template
import random

app = Flask(__name__)
CORS(app)

# Get OpenRouter API key from environment variable
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_openrouter_api(prompt, system_prompt):
    """Real OpenRouter API call with DeepSeek v3"""
    if not OPENROUTER_API_KEY:
        raise Exception("OpenRouter API key not found in environment variables")
    
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://nipa-ai.com',
        'X-Title': 'Nipa AI'
    }
    
    # Enhanced system prompt to ensure emojis instead of asterisks
    enhanced_system_prompt = f"{system_prompt} CRITICAL: Never use asterisks (*) for emphasis. Always use emojis like 💕✨🌟💖🎀💄👗🛍️ instead. Replace any asterisks with appropriate emojis."
    
    payload = {
        'model': 'deepseek/deepseek-chat',
        'messages': [
            {'role': 'system', 'content': enhanced_system_prompt},
            {'role': 'user', 'content': f"{prompt} (Please use emojis instead of asterisks for all emphasis and formatting)"}
        ],
        'temperature': 0.7,
        'max_tokens': 500,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    
    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        # Replace any remaining asterisks with sparkle emojis
        return ai_response.replace('*', '✨')
    else:
        error_msg = f"OpenRouter API Error: {response.status_code} - {response.text}"
        print(error_msg)
        raise Exception(error_msg)


@app.route('/')
def index():
    """Serve the main Nipa website"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint for Nipa AI using real OpenRouter API"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        system_prompt = data.get('system_prompt', "You are Nipa, a helpful AI assistant for girls. You're friendly, supportive, and knowledgeable about fashion, beauty, wellness, and lifestyle. IMPORTANT: Always use emojis instead of asterisks (*). Never use asterisks for emphasis - use emojis like 💕✨🌟💖 instead. Respond in a girly, encouraging tone with lots of emojis.")
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Call real OpenRouter API
        ai_response = call_openrouter_api(message, system_prompt)
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Chat API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/fashion/outfit', methods=['POST'])
def generate_outfit():
    """Generate outfit recommendations using real AI"""
    try:
        data = request.get_json()
        occasion = data.get('occasion', '')
        weather = data.get('weather', '')
        style = data.get('style', '')
        
        if not all([occasion, weather, style]):
            return jsonify({'error': 'All fields are required'}), 400
        
        prompt = f"Create a detailed outfit recommendation for a {style} style, {occasion} occasion, in {weather} weather. Include specific clothing items, colors, accessories, and styling tips. Make it girly and fashionable with lots of emojis!"
        
        system_prompt = "You are a professional fashion stylist AI for girls. Provide detailed, practical outfit recommendations with specific items, colors, and styling tips. Be enthusiastic and use LOTS of emojis like 👗💄✨🌟💕👠💎🎀. Never use asterisks - only emojis for emphasis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        
        return jsonify({'outfit': ai_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Fashion API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/beauty/skincare', methods=['POST'])
def generate_skincare_routine():
    """Generate personalized skincare routine using real AI"""
    try:
        data = request.get_json()
        skin_type = data.get('skin_type', '')
        concerns = data.get('concerns', '')
        budget = data.get('budget', '')
        
        if not all([skin_type, concerns, budget]):
            return jsonify({'error': 'All fields are required'}), 400
        
        prompt = f"Create a personalized skincare routine for {skin_type} skin with {concerns} concerns, within a {budget} budget. Include morning and evening routines, specific product recommendations, and application tips with lots of emojis!"
        
        system_prompt = "You are a skincare expert AI for girls. Provide detailed, personalized skincare routines with specific product recommendations, application order, and helpful tips. Be encouraging and use LOTS of emojis like 💄🧴✨🌟💕🥒🌸. Never use asterisks - only emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        
        return jsonify({'routine': ai_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Beauty API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/wellness/cycle', methods=['POST'])
def calculate_cycle():
    """Calculate menstrual cycle predictions"""
    try:
        data = request.get_json()
        last_period = data.get('last_period', '')
        cycle_length = int(data.get('cycle_length', 28))
        
        if not last_period:
            return jsonify({'error': 'Last period date is required'}), 400
        
        # Parse the date
        last_period_date = datetime.strptime(last_period, '%Y-%m-%d')
        
        # Calculate predictions
        next_period = last_period_date + timedelta(days=cycle_length)
        ovulation = last_period_date + timedelta(days=cycle_length - 14)
        fertile_start = ovulation - timedelta(days=5)
        fertile_end = ovulation + timedelta(days=1)
        
        return jsonify({
            'next_period': next_period.isoformat(),
            'ovulation': ovulation.isoformat(),
            'fertile_start': fertile_start.isoformat(),
            'fertile_end': fertile_end.isoformat()
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"Cycle API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/wellness/workout', methods=['POST'])
def generate_workout_plan():
    """Generate personalized workout plan using real AI"""
    try:
        data = request.get_json()
        goal = data.get('goal', '')
        time = data.get('time', '')
        
        if not all([goal, time]):
            return jsonify({'error': 'All fields are required'}), 400
        
        prompt = f"Create a {time}-minute daily workout plan for {goal}. Include specific exercises, sets, reps, and modifications for beginners. Make it female-focused and motivating with lots of emojis!"
        
        system_prompt = "You are a fitness trainer AI specializing in women's fitness. Provide detailed, safe, and effective workout plans with clear instructions and motivational language. Use LOTS of emojis like 💪🏃‍♀️✨🌟💕🔥💦. Never use asterisks - only emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        
        return jsonify({'workout': ai_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Workout API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/lifestyle/mood', methods=['POST'])
def handle_mood():
    """Handle mood tracking and response using real AI"""
    try:
        data = request.get_json()
        mood = data.get('mood', '')
        emoji = data.get('emoji', '')
        
        if not mood:
            return jsonify({'error': 'Mood is required'}), 400
        
        prompt = f"The user is feeling {mood} today {emoji}. Provide a supportive, encouraging response with personalized advice, self-care tips, or activities that match their mood. Keep it girly and uplifting with lots of emojis!"
        
        system_prompt = "You are a supportive friend AI for girls. Provide empathetic, encouraging responses with practical self-care advice based on the user's mood. Be warm, understanding, and use LOTS of emojis like 💕✨🌟💖🤗🌸. Never use asterisks - only emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Mood API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/lifestyle/affirmation', methods=['GET'])
def generate_affirmation():
    """Generate daily affirmation using real AI"""
    try:
        prompt = "Generate a powerful, uplifting daily affirmation for girls. Make it personal, encouraging, and full of positive energy with beautiful emojis!"
        
        system_prompt = "You are a motivational coach AI for girls. Create inspiring, personalized affirmations that boost confidence and self-love. Use beautiful emojis like 💖✨🌟👑💕🦋. Never use asterisks - only emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        
        return jsonify({'affirmation': ai_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Affirmation API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/lifestyle/selfcare', methods=['POST'])
def generate_selfcare():
    """Generate self-care routine using real AI"""
    try:
        data = request.get_json()
        time = data.get('time', '')
        
        if not time:
            return jsonify({'error': 'Time is required'}), 400
        
        prompt = f"Create a {time}-minute self-care routine for girls. Include specific activities, products, and steps that promote relaxation and self-love. Make it detailed and luxurious with lots of emojis!"
        
        system_prompt = "You are a self-care expert AI for girls. Provide detailed, relaxing self-care routines with specific steps and recommendations. Be nurturing and use LOTS of emojis like 🛁💆‍♀️✨🌸💕🕯️. Never use asterisks - only emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        
        return jsonify({'routine': ai_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Self-care API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/shopping/products', methods=['POST'])
def find_products():
    """Find product recommendations using real AI"""
    try:
        data = request.get_json()
        category = data.get('category', '')
        budget = data.get('budget', '')
        specific = data.get('specific', '')
        
        if not all([category, budget]):
            return jsonify({'error': 'Category and budget are required'}), 400
        
        prompt = f"Find the best {category} products within {budget} budget{' specifically for \"' + specific + '\"' if specific else ''}. Include product names, price ranges, where to buy, and why they're great. Focus on quality and value with lots of emojis!"
        
        system_prompt = "You are a shopping expert AI for girls. Provide detailed product recommendations with prices, where to buy, and honest reviews. Be helpful and enthusiastic with LOTS of emojis like 🛍️💎✨🌟💕💄👗. Never use asterisks - only emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        
        return jsonify({'products': ai_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Shopping API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/community/question', methods=['POST'])
def handle_anonymous_question():
    """Handle anonymous community questions using real AI"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        prompt = f"Answer this anonymous question from a girl: \"{question}\". Provide supportive, non-judgmental advice with empathy and understanding. Be like a caring big sister with lots of emojis!"
        
        system_prompt = "You are a supportive community moderator AI for girls. Provide caring, non-judgmental advice to anonymous questions. Be empathetic, understanding, and like a caring big sister with LOTS of emojis like 💕✨🌟💖🤗👭. Never use asterisks - only emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Community API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/community/girl-talk', methods=['GET'])
def generate_girl_talk_topic():
    """Generate girl talk discussion topic using real AI"""
    try:
        prompt = "Generate an engaging, fun discussion topic for girls to chat about. Make it relatable, positive, and something that encourages sharing and bonding. Include emojis!"
        
        system_prompt = "You are a community engagement AI for girls. Create fun, engaging discussion topics that promote positive conversations and bonding. Use emojis like 💬👭✨💕🌟. Never use asterisks - only emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        
        return jsonify({'topic': ai_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Girl Talk API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

@app.route('/api/community/style-challenge', methods=['GET'])
def generate_style_challenge():
    """Generate weekly style challenge using real AI"""
    try:
        prompt = "Create a fun, creative weekly style challenge for girls. Make it achievable, inspiring, and encourage creativity and self-expression. Include specific instructions and lots of emojis!"
        
        system_prompt = "You are a fashion challenge creator AI for girls. Design fun, achievable style challenges that promote creativity and confidence. Use emojis like 👗✨🏆💕🌟📸. Never use asterisks - only emojis."
        
        ai_response = call_openrouter_api(prompt, system_prompt)
        
        return jsonify({'challenge': ai_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Style Challenge API Error: {error_msg}")
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    if not OPENROUTER_API_KEY:
        print("WARNING: OPENROUTER_API_KEY environment variable not set!")
        print("Please set your OpenRouter API key: export OPENROUTER_API_KEY='your-key-here'")
    else:
        print("✅ OpenRouter API key found! Starting Nipa AI server...")
    
    app.run(debug=True, host='0.0.0.0', port=5000)