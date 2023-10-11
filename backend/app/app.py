from flask import Flask, render_template, request, Blueprint, jsonify, session
from views import api_bp
import jwt

app = Flask(__name__)
messages = []
# Set Flask application key to use session
app.secret_key = 'ilovebupt'

@app.route('/')
def home():
    return render_template('index.html')

# register the blueprint from views.py
app.register_blueprint(api_bp, prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=11451)