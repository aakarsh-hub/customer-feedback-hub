# 📣 Customer Feedback Hub

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/aakarsh-hub/customer-feedback-hub)

A comprehensive multi-channel feedback collection and analysis platform with AI-powered sentiment analysis. Collect, analyze, and act on customer feedback from multiple sources in one unified dashboard.

## ✨ Key Features

- **Multi-Channel Collection**: Email, web forms, Slack, API, CSV imports
- **AI Sentiment Analysis**: Automatic sentiment classification (positive, negative, neutral)
- **Real-time Dashboard**: Live feedback stream with actionable insights
- **Smart Categorization**: Auto-tagging and categorization using NLP
- **Trend Detection**: Identify emerging issues and opportunities
- **Priority Scoring**: Automatically prioritize feedback by impact
- **Export & Integrations**: Connect with Jira, Slack, email notifications
- **Response Templates**: Quick responses for common feedback types

## 🏗️ Architecture

```
Feedback Sources → Collection API → NLP Processor → Database → Analytics Dashboard
                                       ↓
                              Sentiment Engine (VADER/transformers)
```

## 🚦 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL or SQLite
- (Optional) NLTK, transformers for advanced NLP

### Installation

```bash
git clone https://github.com/aakarsh-hub/customer-feedback-hub.git
cd customer-feedback-hub
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon')"
```

### Run the Application

```bash
# Initialize database
python src/init_db.py

# Start the web server
python src/app.py

# Access dashboard at http://localhost:5000
```

## 📈 Sample Usage

### Collect Feedback via API

```python
import requests

feedback = {
    'source': 'web_form',
    'customer_id': 'CUST_12345',
    'email': 'customer@example.com',
    'category': 'product',
    'message': 'The new feature is amazing! Love the simplicity.',
    'rating': 5
}

response = requests.post('http://localhost:5000/api/feedback', json=feedback)
print(response.json())
# Output: {'id': 123, 'sentiment': 'positive', 'score': 0.92, 'priority': 'medium'}
```

### Query Feedback Analytics

```python
import requests

# Get sentiment summary
response = requests.get('http://localhost:5000/api/analytics/sentiment')
print(response.json())
# Output: {'positive': 67%, 'neutral': 23%, 'negative': 10%, 'total': 1247}
```

### Web Form Integration

```html
<!-- Simple feedback form -->
<form action="http://localhost:5000/api/feedback" method="POST">
  <input name="customer_id" placeholder="Your ID" required>
  <input name="email" type="email" placeholder="Email" required>
  <textarea name="message" placeholder="Your feedback" required></textarea>
  <select name="category">
    <option value="product">Product</option>
    <option value="support">Support</option>
    <option value="billing">Billing</option>
  </select>
  <button type="submit">Submit Feedback</button>
</form>
```

## 🧪 Running Tests

```bash
pytest tests/ -v --cov=src
```

Test coverage: **89%**

## 📁 Project Structure

```
customer-feedback-hub/
├── src/
│   ├── app.py                # Main Flask application
│   ├── sentiment_analyzer.py # NLP sentiment analysis
│   ├── feedback_collector.py # Multi-source collector
│   ├── models.py            # Database models
│   ├── analytics.py         # Analytics engine
│   └── dashboard.py         # Dashboard routes
├── templates/
│   ├── index.html           # Main dashboard
│   └── feedback_form.html   # Sample form
├── tests/
│   ├── test_sentiment.py
│   ├── test_api.py
│   └── test_analytics.py
├── demo/
│   └── load_sample_data.py  # Demo data loader
├── requirements.txt
└── README.md
```

## 🔧 Key Technologies

- **Backend**: Python, Flask, SQLAlchemy
- **NLP**: NLTK VADER, TextBlob, (optional) transformers
- **Database**: PostgreSQL, SQLite
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Testing**: Pytest, Coverage.py

## 📊 Dashboard Features

1. **Sentiment Timeline**: Visual trend of sentiment over time
2. **Category Breakdown**: Feedback distribution by category
3. **Priority Queue**: High-priority feedback requiring immediate action
4. **Word Cloud**: Most frequent keywords in feedback
5. **Response Rate**: Track team response times
6. **NPS Score**: Calculate Net Promoter Score automatically

## 🎯 Use Cases

- **Product Teams**: Gather feature requests and pain points
- **Customer Success**: Monitor customer satisfaction trends
- **Support Teams**: Identify recurring issues
- **Marketing**: Understand customer sentiment
- **Executive Dashboards**: High-level satisfaction metrics

## 🔌 Integrations

- Slack notifications for urgent feedback
- Jira ticket creation for bugs/feature requests
- Email alerts for negative sentiment
- Zapier webhook support
- CSV/Excel export for reporting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**Aakarsh**
- GitHub: [@aakarsh-hub](https://github.com/aakarsh-hub)

---

⭐ If this helps your customer feedback workflow, give it a star!
