# ================================
# Password Strength Checker
# DecodeLabs - Project 1
# Flask Web Application
# ================================

from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Common weak passwords list
COMMON_PASSWORDS = [
    "password", "123456", "password123", "admin", "letmein",
    "qwerty", "abc123", "monkey", "1234567890", "password1"
]

def check_password_strength(password):
    suggestions = []
    score = 0

    # Check common passwords
    if password.lower() in COMMON_PASSWORDS:
        return {
            "score": 0,
            "strength": "VERY WEAK",
            "suggestions": ["❌ This is a very common password. Choose something unique!"]
        }

    # Check length
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("❌ Use at least 8 characters")

    # Check uppercase
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        suggestions.append("❌ Add at least one uppercase letter")

    # Check lowercase
    if re.search(r'[a-z]', password):
        score += 1
    else:
        suggestions.append("❌ Add at least one lowercase letter")

    # Check numbers
    if re.search(r'[0-9]', password):
        score += 1
    else:
        suggestions.append("❌ Add at least one number")

    # Check symbols
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        score += 1
    else:
        suggestions.append("❌ Add at least one special character (!@#$...)")

    # Classify strength
    if score == 5:
        strength = "STRONG"
    elif score >= 3:
        strength = "MEDIUM"
    elif score >= 2:
        strength = "WEAK"
    else:
        strength = "VERY WEAK"

    if not suggestions:
        suggestions.append("✅ Great password! Keep it safe.")

    return {
        "score": score,
        "strength": strength,
        "suggestions": suggestions
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    password = data.get('password', '')
    result = check_password_strength(password)
    return jsonify(result)

if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)
    