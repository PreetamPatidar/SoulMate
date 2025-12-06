// Authentication handling
const API_BASE = 'http://localhost:8000/api';

class AuthManager {
    constructor() {
        this.token = localStorage.getItem('access_token');
        this.refreshToken = localStorage.getItem('refresh_token');
        this.user = null;

        this.init();
    }

    init() {
        // Tab switching
        document.getElementById('login-tab').addEventListener('click', () => this.switchTab('login'));
        document.getElementById('register-tab').addEventListener('click', () => this.switchTab('register'));

        // Form submissions
        document.getElementById('login-form').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('register-form').addEventListener('submit', (e) => this.handleRegister(e));

        // Check if already logged in
        if (this.token) {
            this.verifyToken();
        }
    }

    switchTab(tab) {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));

        document.getElementById(`${tab}-tab`).classList.add('active');
        document.getElementById(`${tab}-form`).classList.add('active');
    }

    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        try {
            const response = await fetch(`${API_BASE}/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                this.setTokens(data.tokens);
                this.user = data.user;
                this.showChatScreen();
            } else {
                this.showMessage(data.error || 'Login failed');
            }
        } catch (error) {
            this.showMessage('Network error. Please try again.');
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;

        try {
            const response = await fetch(`${API_BASE}/auth/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                this.setTokens(data.tokens);
                this.user = data.user;
                this.showChatScreen();
            } else {
                this.showMessage(Object.values(data).flat().join(', '));
            }
        } catch (error) {
            this.showMessage('Network error. Please try again.');
        }
    }

    async verifyToken() {
        try {
            const response = await fetch(`${API_BASE}/users/profile/`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                this.user = data;
                this.showChatScreen();
            } else {
                this.logout();
            }
        } catch (error) {
            this.logout();
        }
    }

    setTokens(tokens) {
        this.token = tokens.access;
        this.refreshToken = tokens.refresh;
        localStorage.setItem('access_token', this.token);
        localStorage.setItem('refresh_token', this.refreshToken);
    }

    logout() {
        this.token = null;
        this.refreshToken = null;
        this.user = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        this.showLoginScreen();
    }

    showLoginScreen() {
        document.getElementById('login-screen').classList.add('active');
        document.getElementById('chat-screen').classList.remove('active');
    }

    showChatScreen() {
        document.getElementById('login-screen').classList.remove('active');
        document.getElementById('chat-screen').classList.add('active');
        chatManager.init();
    }

    showMessage(message) {
        const messageEl = document.getElementById('auth-message');
        messageEl.textContent = message;
        messageEl.style.color = 'red';
    }
}

const authManager = new AuthManager();
