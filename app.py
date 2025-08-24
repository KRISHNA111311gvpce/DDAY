from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import sys
import os

# Add the current directory to the path so we can import your blockchain code
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your blockchain functions
from bell_9 import (
    users, balances, blockchain, network_stats, 
    create_transaction, refresh_balance, generate_wallet,
    quantum_keys, quantum_dimension
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    """Return all users and their balances"""
    user_data = {}
    for key, user in users.items():
        user_data[key] = {
            'username': user['username'],
            'public_key': user['public_key'],
            'balance': balances.get(user['public_key'], 0),
            'has_quantum_key': quantum_keys[key] is not None
        }
    return jsonify(user_data)

@app.route('/api/blockchain', methods=['GET'])
def get_blockchain():
    """Return the blockchain"""
    return jsonify(blockchain)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Return network statistics"""
    return jsonify(network_stats)

@app.route('/api/transaction', methods=['POST'])
def create_tx():
    """Create a new transaction"""
    data = request.json
    sender_key = data.get('sender')
    receiver_key = data.get('receiver')
    amount = data.get('amount')
    
    if not all([sender_key, receiver_key, amount]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    if sender_key not in users:
        return jsonify({'error': 'Sender not found'}), 404
        
    if receiver_key not in users:
        return jsonify({'error': 'Receiver not found'}), 404
    
    sender_wallet = users[sender_key]
    
    # Create the transaction
    tx = create_transaction(
        sender_wallet['private_key'],
        users[receiver_key]['public_key'],
        amount
    )
    
    if tx:
        return jsonify({
            'success': True,
            'transaction': tx,
            'message': 'Transaction completed successfully'
        })
    else:
        return jsonify({'error': 'Transaction failed'}), 500

@app.route('/api/quantum-dimension', methods=['GET'])
def get_quantum_dimension():
    """Get the current quantum dimension setting"""
    return jsonify({'dimension': quantum_dimension})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
