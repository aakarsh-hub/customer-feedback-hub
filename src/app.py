"""Customer Feedback Hub - Main Application

Multi-channel feedback collection with sentiment analysis.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import json

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Database Models
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))
    customer_id = db.Column(db.String(100))
    email = db.Column(db.String(200))
    category = db.Column(db.String(50))
    message = db.Column(db.Text)
    rating = db.Column(db.Integer)
    sentiment = db.Column(db.String(20))
    sentiment_score = db.Column(db.Float)
    priority = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
with app.app_context():
    db.create_all()

def analyze_sentiment(text):
    """Analyze sentiment of text using VADER"""
    scores = sentiment_analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        sentiment = 'positive'
    elif compound <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return sentiment, compound

def calculate_priority(sentiment, rating, message_length):
    """Calculate feedback priority"""
    if sentiment == 'negative' or (rating and rating <= 2):
        return 'high'
    elif sentiment == 'positive' or (rating and rating >= 4):
        return 'low'
    else:
        return 'medium'

@app.route('/')
def index():
    """Dashboard home"""
    return jsonify({
        'name': 'Customer Feedback Hub',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': [
            '/api/feedback - POST: Submit feedback',
            '/api/feedback - GET: Retrieve feedback',
            '/api/analytics/sentiment - GET: Sentiment analysis',
            '/api/analytics/categories - GET: Category breakdown'
        ]
    })

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit new feedback"""
    try:
        data = request.json
        message = data.get('message', '')
        
        # Analyze sentiment
        sentiment, score = analyze_sentiment(message)
        
        # Calculate priority
        priority = calculate_priority(
            sentiment, 
            data.get('rating'),
            len(message)
        )
        
        # Create feedback entry
        feedback = Feedback(
            source=data.get('source', 'api'),
            customer_id=data.get('customer_id'),
            email=data.get('email'),
            category=data.get('category', 'general'),
            message=message,
            rating=data.get('rating'),
            sentiment=sentiment,
            sentiment_score=score,
            priority=priority
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'id': feedback.id,
            'sentiment': sentiment,
            'score': round(score, 2),
            'priority': priority,
            'message': 'Feedback submitted successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    """Retrieve feedback with filters"""
    category = request.args.get('category')
    sentiment = request.args.get('sentiment')
    priority = request.args.get('priority')
    limit = int(request.args.get('limit', 50))
    
    query = Feedback.query
    
    if category:
        query = query.filter_by(category=category)
    if sentiment:
        query = query.filter_by(sentiment=sentiment)
    if priority:
        query = query.filter_by(priority=priority)
    
    feedbacks = query.order_by(Feedback.created_at.desc()).limit(limit).all()
    
    return jsonify([
        {
            'id': f.id,
            'source': f.source,
            'customer_id': f.customer_id,
            'category': f.category,
            'message': f.message,
            'rating': f.rating,
            'sentiment': f.sentiment,
            'priority': f.priority,
            'created_at': f.created_at.isoformat()
        }
        for f in feedbacks
    ])

@app.route('/api/analytics/sentiment', methods=['GET'])
def get_sentiment_analytics():
    """Get sentiment distribution"""
    total = Feedback.query.count()
    positive = Feedback.query.filter_by(sentiment='positive').count()
    negative = Feedback.query.filter_by(sentiment='negative').count()
    neutral = Feedback.query.filter_by(sentiment='neutral').count()
    
    return jsonify({
        'total': total,
        'positive': positive,
        'positive_percent': round(positive / total * 100, 1) if total > 0 else 0,
        'negative': negative,
        'negative_percent': round(negative / total * 100, 1) if total > 0 else 0,
        'neutral': neutral,
        'neutral_percent': round(neutral / total * 100, 1) if total > 0 else 0
    })

@app.route('/api/analytics/categories', methods=['GET'])
def get_category_analytics():
    """Get category breakdown"""
    categories = db.session.query(
        Feedback.category,
        db.func.count(Feedback.id).label('count')
    ).group_by(Feedback.category).all()
    
    return jsonify([
        {'category': cat, 'count': count}
        for cat, count in categories
    ])

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Customer Feedback Hub")
    print("  Server running on http://localhost:5000")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
