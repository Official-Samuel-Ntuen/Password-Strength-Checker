// ================================
// DecodeLabs - Password Checker
// JavaScript Logic
// ================================

// Toggle password visibility
function togglePassword() {
    const input = document.getElementById('passwordInput');
    input.type = input.type === 'password' ? 'text' : 'password';
}

// Check password strength
async function checkPassword() {
    const password = document.getElementById('passwordInput').value;
    const strengthBar = document.getElementById('strengthBar');
    const strengthLabel = document.getElementById('strengthLabel');
    const scoreText = document.getElementById('scoreText');
    const suggestions = document.getElementById('suggestions');

    // If empty reset everything
    if (password.length === 0) {
        strengthBar.style.width = '0%';
        strengthLabel.textContent = 'Enter a password to check';
        scoreText.textContent = '0';
        suggestions.innerHTML = '';
        return;
    }

    // Send password to Flask backend
    const response = await fetch('/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: password })
    });

    const result = await response.json();

    // Update score
    scoreText.textContent = result.score;

    // Update strength bar color and width
    const percentage = (result.score / 5) * 100;
    strengthBar.style.width = percentage + '%';

    if (result.strength === 'STRONG') {
        strengthBar.style.background = '#00ff88';
        strengthLabel.style.color = '#00ff88';
    } else if (result.strength === 'MEDIUM') {
        strengthBar.style.background = '#ffaa00';
        strengthLabel.style.color = '#ffaa00';
    } else if (result.strength === 'WEAK') {
        strengthBar.style.background = '#ff6600';
        strengthLabel.style.color = '#ff6600';
    } else {
        strengthBar.style.background = '#ff0044';
        strengthLabel.style.color = '#ff0044';
    }

    // Update strength label
    strengthLabel.textContent = '🔐 Strength: ' + result.strength;

    // Update suggestions
    suggestions.innerHTML = '';
    result.suggestions.forEach(suggestion => {
        const p = document.createElement('p');
        p.textContent = suggestion;
        suggestions.appendChild(p);
    });
}