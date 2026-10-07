import requests
from flask import Blueprint, request, jsonify, current_app
from app.models import SiteSetting

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'status': 'error', 'reply': 'Please enter a valid message.'}), 400

    api_key = current_app.config.get('GEMINI_API_KEY', '').strip()
    config_model = current_app.config.get('GEMINI_MODEL', 'gemini-3-flash-preview').strip()

    # Load context dynamically from site settings if available
    try:
        settings = {s.key: s.value for s in SiteSetting.query.all()}
    except Exception:
        settings = {}

    school_name = settings.get('school_name', 'XYZ School and College')
    school_address = settings.get('school_address', 'Bafal, Kathmandu, Nepal')
    school_phone = settings.get('school_phone', '+977 98511-59700')
    school_email = settings.get('school_email', 'info@xyzschool.edu.np')
    principal_name = settings.get('principal_name', 'Ramesh S. Shrestha')
    chairperson_name = settings.get('chairperson_name', 'Mr. Indra Bahadur Maharjan')

    system_prompt = f"""System Context:
You are the official AI Assistant for {school_name}, located in {school_address}.
Your goal is to answer user questions politely, directly, and accurately using the details below.

School Information:
- School Name: {school_name}
- Location / Address: {school_address}
- Phone: {school_phone}
- Email: {school_email}
- Principal: {principal_name}
- SMC Chairperson: {chairperson_name}
- Academic Streams & Levels: Pre-Primary (Montessori), Basic Level (Grades 1 to 8), Secondary & Higher Secondary (+2 Science, Management, and Technical Education).
- Campus Facilities: Computer Lab with internet & IT instructors, Science Labs (Physics, Chemistry, Biology), Library, Sports & Physical Training Grounds.
- Admissions: Online admission inquiry form is available on the website portal.

Instructions for AI Response:
- Read and answer the user's specific question directly and accurately based on the context provided above.
- If asked general educational or school questions, provide a helpful and warm response.
- Format your response cleanly using bullet points or paragraphs where appropriate.

User Question: {user_message}"""

    # Primary model and list of fallback models
    models_to_try = [config_model, 'gemini-3-flash-preview', 'gemini-3.8-flash', 'gemini-3.5-flash-lite', 'gemini-2.5-pro', 'gemini-flash-latest']
    seen_models = set()

    if api_key and api_key != 'YOUR_GEMINI_API_KEY_HERE':
        for model_name in models_to_try:
            if not model_name or model_name in seen_models:
                continue
            seen_models.add(model_name)

            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": system_prompt}]
                    }]
                }

                response = requests.post(url, json=payload, headers=headers, timeout=12)
                if response.status_code == 200:
                    res_data = response.json()
                    try:
                        bot_reply = res_data['candidates'][0]['content']['parts'][0]['text']
                        if bot_reply and bot_reply.strip():
                            return jsonify({'status': 'success', 'reply': bot_reply.strip()})
                    except (KeyError, IndexError):
                        pass
                else:
                    current_app.logger.warning(f"Gemini model {model_name} returned status {response.status_code}: {response.text}")
            except Exception as e:
                current_app.logger.error(f"Gemini API Exception for model {model_name}: {e}")

    # Fallback response if API key is invalid, missing, or all API requests fail
    msg_lower = user_message.lower()
    if any(k in msg_lower for k in ['admission', 'apply', 'enroll', 'join']):
        fallback = f"Admissions are open at {school_name}! You can submit an online inquiry using the 'Admission Inquiry' button in the menu bar or contact our office at {school_phone}."
    elif any(k in msg_lower for k in ['fee', 'cost', 'charge', 'price']):
        fallback = f"For detailed fee structures across Pre-Primary, Basic, and Secondary (+2) levels, please contact our administration at {school_phone} or email {school_email}."
    elif any(k in msg_lower for k in ['course', 'academic', 'subject', 'class', 'grade', 'stream']):
        fallback = f"{school_name} offers Montessori Pre-Primary, Basic Level (Grades 1-8), and Secondary (+2) streams in Science, Management, and Technical Education with modern lab facilities."
    elif any(k in msg_lower for k in ['facility', 'lab', 'computer', 'library', 'sports']):
        fallback = f"Our campus in {school_address} features state-of-the-art Computer and Science laboratories, a digital library, interactive classrooms, and multi-sports grounds."
    elif any(k in msg_lower for k in ['contact', 'phone', 'email', 'location', 'address']):
        fallback = f"{school_name} is located at {school_address}. Phone: {school_phone} | Email: {school_email}."
    else:
        fallback = f"Welcome to {school_name}, {school_address}. How can I assist you today? You can ask about our academic programs, admissions, campus facilities, or contact info."

    return jsonify({'status': 'success', 'reply': fallback})
