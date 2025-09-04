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

# OpenRouter API configuration (replace with your actual API key)
OPENROUTER_API_KEY = "your-openrouter-api-key-here"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_openrouter_api(prompt, system_prompt):
    """Helper function to call OpenRouter API with emoji-focused prompting"""
    try:
        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
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
            'max_tokens': 500
        }
        
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            # Replace any remaining asterisks with sparkle emojis
            return ai_response.replace('*', '✨')
        else:
            return generate_fallback_response(prompt)
            
    except Exception as e:
        print(f"OpenRouter API Error: {e}")
        return generate_fallback_response(prompt)

def generate_fallback_response(prompt):
    """Generate intelligent fallback responses when API is unavailable"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['fashion', 'outfit', 'clothes', 'dress', 'style']):
        responses = [
            "OMG yes! Fashion is my absolute favorite topic! 👗✨ I'd love to help you put together the perfect outfit! What's the occasion? Are you going for cute and casual, or something more glam? I have so many ideas brewing! 💕🌟",
            "Fashion talk! 💄✨ I'm so excited to help you look absolutely stunning! Whether it's casual chic or glamorous goddess vibes, I've got the perfect styling tips for you! What kind of look are you going for? 👗💕",
            "Yay! Let's create some fashion magic together! ✨👗 I love helping girls find their perfect style! Tell me about the occasion and your personal style preferences - I have so many cute ideas! 💕🌟"
        ]
    elif any(word in prompt_lower for word in ['beauty', 'makeup', 'skincare', 'cosmetics']):
        responses = [
            "Beauty talk! 💄✨ I'm so here for this! Whether it's skincare routines, makeup tips, or finding the perfect products for your skin type, I've got you covered babe! What beauty goals are we working on today? 🌟💕",
            "OMG I love beauty conversations! 💋✨ From glowing skin to perfect makeup looks, I'm here to help you feel absolutely gorgeous! What's your current beauty routine like? Let's make it even more amazing! 💕🌟",
            "Beauty queen! 👑💄 I'm so excited to help you with all things beauty! Whether you're a makeup newbie or a total pro, I have tips and tricks that'll make you shine! What would you like to focus on? ✨💕"
        ]
    elif any(word in prompt_lower for word in ['sad', 'down', 'upset', 'depressed', 'crying']):
        responses = [
            "Aww honey, I'm here for you! 🤗💕 It's totally okay to feel this way sometimes. You're amazing and this feeling will pass! Want to talk about what's bothering you? Or maybe we could plan some self-care activities to lift your spirits? ✨🌸",
            "Sweet girl, sending you the biggest virtual hug right now! 🤗💕 Remember that you're stronger than you know and this tough moment won't last forever. I'm here to listen and support you through this! ✨💖",
            "Oh babe, my heart goes out to you! 💕🌸 It's completely normal to have these feelings, and you're so brave for reaching out. Let's focus on some gentle self-care and positive vibes together! You've got this! ✨🤗"
        ]
    elif any(word in prompt_lower for word in ['happy', 'excited', 'great', 'amazing', 'wonderful']):
        responses = [
            "Yay! I love your positive energy! 🥰✨ You're absolutely glowing today! What's making you feel so amazing? I'm so here for all the good vibes! Let's keep this happiness flowing! 💕🌟",
            "This is so wonderful to hear! 🌟💕 Your happiness is absolutely contagious! I'm beaming with joy for you right now! Tell me all about what's making your day so special! ✨🥰",
            "OMG yes! I'm literally dancing with joy for you! 💃✨ Your positive energy is everything! I love seeing you so happy and radiant! What's the secret to your amazing mood today? 💕🌟"
        ]
    elif any(word in prompt_lower for word in ['workout', 'fitness', 'exercise', 'gym']):
        responses = [
            "Yes queen! 💪✨ I love that you're prioritizing your health and wellness! Whether you want a quick 15-minute routine or a full workout plan, I can help you find something that fits your goals and schedule! What kind of vibe are you going for? 🏃‍♀️💕",
            "Fitness goddess! 🏃‍♀️✨ I'm so proud of you for taking care of your body! From yoga flows to strength training, I have so many fun workout ideas! What's your fitness goal right now? 💪💕",
            "Work it girl! 💪🌟 I absolutely love your dedication to staying healthy and strong! Let's find the perfect workout routine that makes you feel amazing! What type of exercise makes you happiest? ✨💕"
        ]
    elif any(word in prompt_lower for word in ['relationship', 'boyfriend', 'dating', 'love']):
        responses = [
            "Girl, let's talk! 💕✨ Relationships can be so complex but also so beautiful! I'm here to listen and give you the best advice I can. Remember, you deserve someone who treats you like the queen you are! 👑💖 What's on your mind?",
            "Relationship talk! 💕👑 I'm all ears babe! Whether it's butterflies and rainbows or you need to vent, I'm here for all of it! You deserve nothing but the absolute best in love! What's happening in your heart? ✨💖",
            "Love and relationships! 💖✨ This is such an important topic! I'm here to support you through all the ups and downs of matters of the heart! Remember, you're amazing and worthy of incredible love! What would you like to chat about? 💕🌟"
        ]
    elif any(word in prompt_lower for word in ['hi', 'hello', 'hey', 'sup']):
        responses = [
            "Hey gorgeous! 💕✨ I'm so excited to chat with you today! I'm Nipa, your AI bestie who's here to help with anything girly - fashion, beauty, wellness, relationships, or just life in general! What would you love to talk about? 🌟💖",
            "Hello beautiful! 🌟💕 Welcome to our girly chat space! I'm Nipa and I'm absolutely thrilled you're here! Whether you want fashion advice, beauty tips, or just want to chat about life, I'm your girl! What's on your mind today? ✨💖",
            "Hi there stunning! 💖✨ I'm Nipa, your new AI bestie! I'm here to make your day brighter with fashion tips, beauty advice, wellness support, or just some good old girl talk! What would make you smile today? 💕🌟"
        ]
    else:
        responses = [
            "That's such an interesting topic! 💕✨ I love chatting with you about everything and anything! As your AI bestie, I'm here to help make your day a little brighter and more fabulous! Tell me more - I'm all ears! 🌟💖",
            "Ooh, I love where this conversation is going! ✨💕 You always have the most fascinating things to say! I'm here to chat about absolutely anything that's on your mind! What else would you like to explore together? 🌟💖",
            "You're so interesting to talk to! 💖✨ I could chat with you for hours about anything and everything! As your AI bestie, I'm here to listen, support, and share in whatever you'd like to discuss! What's next on your mind? 💕🌟"
        ]
    
    return random.choice(responses)


@app.route('/')
def index():
    """Serve the main Nipa website"""
    return render_template('index.html')

# Main chat endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint for Nipa AI"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        system_prompt = "You are Nipa, a helpful AI assistant for girls. You're friendly, supportive, and knowledgeable about fashion, beauty, wellness, and lifestyle. IMPORTANT: Always use emojis instead of asterisks (*). Never use asterisks for emphasis - use emojis like 💕✨🌟💖 instead. Respond in a girly, encouraging tone with lots of emojis."
        
        # Try OpenRouter API first, fallback to local responses
        if OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your-openrouter-api-key-here":
            ai_response = call_openrouter_api(message, system_prompt)
        else:
            ai_response = generate_fallback_response(message)
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        
        prompt = f"Create a detailed outfit recommendation for a {style} style, {occasion} occasion, in {weather} weather. Include specific clothing items, colors, accessories, and styling tips. Make it girly and fashionable with lots of emojis!"
        
        system_prompt = "You are a professional fashion stylist AI for girls. Provide detailed, practical outfit recommendations with specific items, colors, and styling tips. Be enthusiastic and use LOTS of emojis like 👗💄✨🌟💕👠💎🎀. Never use asterisks - only emojis for emphasis."
        
        if OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your-openrouter-api-key-here":
            ai_response = call_openrouter_api(prompt, system_prompt)
        else:
            # Fallback outfit generation
            outfit_ideas = {
                'casual': {
                    'hot': "Perfect summer casual look! ☀️✨ Try a flowy midi dress in pastel pink or lavender with cute white sneakers! Add a denim jacket for AC spaces, delicate gold jewelry, and a crossbody bag! Don't forget sunglasses and SPF! 👗💕",
                    'mild': "Cozy casual vibes! 🍂✨ Go for high-waisted jeans with a cropped sweater in cream or soft pink! Layer with a cute cardigan, add ankle boots, and finish with a statement necklace! Perfect for coffee dates! 💕👖",
                    'cold': "Winter casual chic! ❄️✨ Try leggings with an oversized sweater, knee-high boots, and a puffer coat in a fun color! Add a beanie, scarf, and warm gloves! Cozy and cute! 🧥💕",
                    'rainy': "Rainy day cuteness! 🌧️✨ Waterproof ankle boots, skinny jeans, a cozy hoodie under a stylish raincoat! Add a cute umbrella and waterproof bag! Stay dry and adorable! ☔💕"
                }
            }
            
            base_response = outfit_ideas.get(occasion, {}).get(weather, "Amazing outfit coming up! ✨💕")
            ai_response = f"{base_response}\n\nStyle tip: Mix textures and don't be afraid to add a pop of your favorite color! Confidence is your best accessory! 👑✨"
        
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
        
        prompt = f"Create a personalized skincare routine for {skin_type} skin with {concerns} concerns, within a {budget} budget. Include morning and evening routines, specific product recommendations, and application tips with lots of emojis!"
        
        system_prompt = "You are a skincare expert AI for girls. Provide detailed, personalized skincare routines with specific product recommendations, application order, and helpful tips. Be encouraging and use LOTS of emojis like 💄🧴✨🌟💕🥒🌸. Never use asterisks - only emojis."
        
        if OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your-openrouter-api-key-here":
            ai_response = call_openrouter_api(prompt, system_prompt)
        else:
            # Fallback skincare routine
            routines = {
                'oily': "Perfect routine for oily skin! ✨💕\n\nMorning: Gentle foaming cleanser, niacinamide serum, lightweight moisturizer, SPF 30+! 🌅\n\nEvening: Double cleanse, BHA 2-3x/week, hydrating serum, night moisturizer! 🌙\n\nTip: Don't over-cleanse - your skin needs balance! 💧✨",
                'dry': "Hydration station for dry skin! 💧✨\n\nMorning: Cream cleanser, hyaluronic acid serum, rich moisturizer, SPF! ☀️\n\nEvening: Oil cleanser, gentle exfoliant 1-2x/week, nourishing serum, night cream! 🌙\n\nTip: Layer your products from thinnest to thickest! 💕",
                'combination': "Balanced approach for combination skin! ⚖️✨\n\nMorning: Gentle gel cleanser, vitamin C serum, lightweight moisturizer, SPF! 🌅\n\nEvening: Micellar water, alternating BHA/AHA, hydrating serum, moisturizer! 🌙\n\nTip: Treat different areas of your face differently! 💕"
            }
            
            ai_response = routines.get(skin_type, "Custom skincare routine coming up! ✨💕 Remember, consistency is key and always patch test new products! Your skin is unique and beautiful! 🌟")
        
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
        
        prompt = f"Create a {time}-minute daily workout plan for {goal}. Include specific exercises, sets, reps, and modifications for beginners. Make it female-focused and motivating with lots of emojis!"
        
        system_prompt = "You are a fitness trainer AI specializing in women's fitness. Provide detailed, safe, and effective workout plans with clear instructions and motivational language. Use LOTS of emojis like 💪🏃‍♀️✨🌟💕🔥💦. Never use asterisks - only emojis."
        
        if OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your-openrouter-api-key-here":
            ai_response = call_openrouter_api(prompt, system_prompt)
        else:
            # Fallback workout plans
            workouts = {
                'weight-loss': f"Fat-burning {time}-minute workout! 🔥💪\n\n• 5 min warm-up (light cardio)\n• 20 min HIIT (30s work, 30s rest)\n• 10 min strength training\n• 5 min cool-down & stretch\n\nYou've got this queen! 💕✨",
                'toning': f"Toning & sculpting {time}-minute routine! 💪✨\n\n• Squats: 3 sets of 15\n• Push-ups: 3 sets of 10\n• Lunges: 3 sets of 12 each leg\n• Plank: 3 sets of 30s\n\nFeel the burn, see the results! 🔥💕",
                'strength': f"Strength building {time}-minute session! 💪🌟\n\n• Compound movements focus\n• Progressive overload\n• Rest 60-90s between sets\n• Form over speed always!\n\nStrong is the new beautiful! 💕✨"
            }
            
            ai_response = workouts.get(goal, f"Amazing {time}-minute workout plan coming up! 💪✨ Remember to listen to your body and stay hydrated! You're doing amazing! 💕🌟")
        
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
        
        prompt = f"The user is feeling {mood} today {emoji}. Provide a supportive, encouraging response with personalized advice, self-care tips, or activities that match their mood. Keep it girly and uplifting with lots of emojis!"
        
        system_prompt = "You are a supportive friend AI for girls. Provide empathetic, encouraging responses with practical self-care advice based on the user's mood. Be warm, understanding, and use LOTS of emojis like 💕✨🌟💖🤗🌸. Never use asterisks - only emojis."
        
        if OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your-openrouter-api-key-here":
            ai_response = call_openrouter_api(prompt, system_prompt)
        else:
            # Fallback mood responses
            mood_responses = {
                'sad': "Sending you the biggest virtual hug! 🤗💕 It's okay to feel sad sometimes - you're human and your feelings are valid! Try some gentle self-care: a warm bath, your favorite tea, or calling a friend. This feeling will pass, beautiful! ✨🌸",
                'happy': "Your happiness is absolutely contagious! 🥰✨ I love seeing you so radiant! Keep spreading those good vibes and maybe treat yourself to something special today - you deserve all the joy! 💕🌟",
                'okay': "Neutral days are totally normal! 💕 Maybe this is the perfect time for some gentle self-care or trying something new? A face mask, a good book, or a walk outside might add some sparkle to your day! ✨🌸",
                'amazing': "YES QUEEN! 👑✨ Your energy is absolutely incredible today! I'm so here for this amazing mood! Whatever you're doing, keep it up because you're absolutely glowing! 💕🌟"
            }
            
            ai_response = mood_responses.get(mood, "Thank you for sharing how you're feeling with me! 💕✨ Remember that all emotions are valid and I'm here to support you no matter what! You're amazing! 🌟💖")
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lifestyle/affirmation', methods=['GET'])
def generate_affirmation():
    """Generate daily affirmation"""
    try:
        affirmations = [
            "You are absolutely radiant and your light shines so bright! ✨💕 Today is going to be amazing because you're in it! 🌟",
            "You are worthy of all the love, success, and happiness in the world! 💖✨ Believe in yourself because you're incredible! 👑",
            "Your strength, beauty, and intelligence inspire everyone around you! 💪💕 You've got this, gorgeous! 🌟",
            "You are enough, exactly as you are right now! ✨💖 Your uniqueness is your superpower! 👑",
            "Today you choose confidence, kindness, and joy! 💕🌟 You're going to make amazing things happen! ✨",
            "You are a queen who deserves to be treated like royalty! 👑💕 Never settle for less than you deserve! ✨",
            "Your dreams are valid and achievable! 🌟💖 Keep believing in yourself because magic happens when you do! ✨"
        ]
        
        affirmation = random.choice(affirmations)
        return jsonify({'affirmation': affirmation})
        
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
        
        selfcare_routines = {
            '5': "Quick 5-minute self-care boost! ✨💕\n\n• Deep breathing (2 min)\n• Gentle face massage\n• Positive affirmations\n• Stretch your neck & shoulders\n\nSmall moments, big impact! 🌟",
            '15': "Perfect 15-minute me-time! 🛁✨\n\n• Cleanse your face\n• Apply a face mask\n• Light a candle\n• Journal 3 things you're grateful for\n• Gentle stretching\n\nYou deserve this time! 💕",
            '30': "Luxurious 30-minute self-care session! 💆‍♀️✨\n\n• Warm bath with essential oils\n• Hair mask treatment\n• Paint your nails\n• Read or listen to music\n• Meditation or yoga\n\nPure bliss awaits! 💕🌟",
            '60': "Ultimate 1-hour pamper session! 👑✨\n\n• Full skincare routine\n• Hair treatment\n• Body scrub & moisturize\n• Manicure & pedicure\n• Relaxing music & tea\n\nYou're worth every minute! 💕",
            '120': "Royal 2+ hour spa day at home! 🏰✨\n\n• Everything above plus:\n• Face mask & eye patches\n• Full body massage (self or partner)\n• Organize your space\n• Plan your week with intention\n\nQueen treatment! 👑💕"
        }
        
        routine = selfcare_routines.get(time, "Custom self-care routine! ✨💕 Remember, any time you spend on yourself is time well invested! You're amazing! 🌟")
        
        return jsonify({'routine': routine})
        
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
        
        prompt = f"Find the best {category} products within {budget} budget{' specifically for \"' + specific + '\"' if specific else ''}. Include product names, price ranges, where to buy, and why they're great. Focus on quality and value with lots of emojis!"
        
        system_prompt = "You are a shopping expert AI for girls. Provide detailed product recommendations with prices, where to buy, and honest reviews. Be helpful and enthusiastic with LOTS of emojis like 🛍️💎✨🌟💕💄👗. Never use asterisks - only emojis."
        
        if OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your-openrouter-api-key-here":
            ai_response = call_openrouter_api(prompt, system_prompt)
        else:
            # Fallback product recommendations
            products = {
                'makeup': f"Amazing {category} finds for {budget}! 💄✨\n\n• Drugstore gems: ELF, NYX, Milani\n• Mid-range favorites: Urban Decay, Too Faced\n• Luxury splurges: Charlotte Tilbury, Pat McGrath\n\nWhere to shop: Ulta, Sephora, Target! 🛍️💕",
                'skincare': f"Perfect {category} products for {budget}! 🧴✨\n\n• Budget-friendly: CeraVe, The Ordinary, Good Molecules\n• Mid-range: Paula's Choice, Drunk Elephant\n• Luxury: La Mer, SK-II\n\nYour skin will thank you! 💕🌟",
                'fashion': f"Stylish {category} picks for {budget}! 👗✨\n\n• Affordable: H&M, Forever 21, ASOS\n• Mid-range: Zara, Mango, & Other Stories\n• Investment: Reformation, Ganni\n\nStyle on any budget! 💕🛍️"
            }
            
            ai_response = products.get(category, f"Great {category} recommendations coming up for {budget}! 🛍️✨ Remember, the best products are ones that make YOU feel amazing! 💕🌟")
        
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
        
        prompt = f"Answer this anonymous question from a girl: \"{question}\". Provide supportive, non-judgmental advice with empathy and understanding. Be like a caring big sister with lots of emojis!"
        
        system_prompt = "You are a supportive community moderator AI for girls. Provide caring, non-judgmental advice to anonymous questions. Be empathetic, understanding, and like a caring big sister with LOTS of emojis like 💕✨🌟💖🤗👭. Never use asterisks - only emojis."
        
        if OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your-openrouter-api-key-here":
            ai_response = call_openrouter_api(prompt, system_prompt)
        else:
            ai_response = "Thank you for trusting us with your question! 💕✨ Remember that you're not alone and your feelings are completely valid. Every girl goes through challenges, and it's okay to ask for help! You're brave for reaching out! 🌟💖 If you need professional support, please don't hesitate to reach out to trusted adults or counselors! 🤗💕"
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/community/girl-talk', methods=['GET'])
def generate_girl_talk_topic():
    """Generate girl talk discussion topic"""
    try:
        topics = [
            "What's your biggest fashion mistake that you actually learned to love? Share your style evolution story! 👗✨💕",
            "If you could give your younger self one piece of advice about confidence, what would it be? 💖🌟",
            "What's the most empowering compliment you've ever received from another girl? Let's spread the love! 💕👭",
            "Share your ultimate self-care Sunday routine! What makes you feel most pampered? 🛁✨",
            "What's a beauty trend you were scared to try but ended up loving? Spill the tea! 💄🌟",
            "If you could have dinner with any inspiring woman, who would it be and what would you ask her? 👑💕",
            "What's your go-to confidence boost when you're feeling down? Share your secrets! ✨💖",
            "Describe your dream girls' night in three emojis and tell us why! 🌟💕",
            "What's the best advice you've gotten from your mom, sister, or female friend? 👭💖",
            "If you could master any skill instantly, what would it be and how would you use it? ✨🌟"
        ]
        
        topic = random.choice(topics)
        return jsonify({'topic': topic})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/community/style-challenge', methods=['GET'])
def generate_style_challenge():
    """Generate weekly style challenge"""
    try:
        challenges = [
            "Color Pop Challenge! 🌈✨ This week, incorporate one bright, bold color into each outfit! Whether it's a statement accessory, lipstick, or a fun top - let your personality shine through color! Share your colorful looks! 💕",
            "Thrift Flip Challenge! ♻️👗 Find one thrifted piece and style it 3 different ways throughout the week! Show us how sustainable fashion can be absolutely stunning! Bonus points for DIY modifications! ✨💕",
            "Confidence Pose Challenge! 📸👑 Each day, take a photo in a pose that makes YOU feel powerful and confident! It's not about perfection - it's about celebrating your unique beauty! Strike a pose, queen! 💕✨",
            "Mix & Match Challenge! 🔄✨ Take 5 pieces from your wardrobe and create 7 different outfits! Show us your creativity and prove that you don't need a huge closet to have amazing style! 👗💕",
            "Accessory Spotlight Challenge! 💎✨ Each day, let one accessory be the star of your outfit! Scarves, jewelry, bags, shoes - show us how the right accessory can transform any look! 💕🌟",
            "Comfort Chic Challenge! 😌👗 Prove that comfortable can be incredibly stylish! Create looks that feel as good as they look - perfect for busy girl life! Comfort is key! ✨💕",
            "Monochrome Magic Challenge! 🎨✨ Pick a different color each day and create a monochromatic look! From soft pastels to bold brights - show us your color story! 💕🌟"
        ]
        
        challenge = random.choice(challenges)
        return jsonify({'challenge': challenge})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)