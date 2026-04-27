# Chicago Personal Travel Agent

A simplified AI-powered travel agent that helps tourists find Chicago hotels based on style preferences, safety considerations, and transit accessibility.

## 🎯 Problem Statement

While many AI travel tools exist, they often fail to have specific user preferences such as "quiet rooms," "proximity to public transportation," and other factors that are verified real-time. Travelers currently spend hours cross-referencing text reviews with photos and transit maps.

## 🚀 Features

- **Multimodal Style Matching**: Upload photos or describe your preferred hotel style to find matches
- **Agentic Architecture**: Specialized agents for style analysis, safety evaluation, and transit accessibility
- **Real-time Data Integration**: Chicago Data Portal API integration for transit and safety data
- **Interactive UI**: Streamlit dashboard with map views and hotel comparison tools
- **Persistent Memory**: User style preferences maintained across sessions
- **RAG System**: Vector database for Chicago neighborhood information

## 🏗️ Architecture (Simplified)

```
├── app.py              # Original rule-based version
├── app_v2.py           # AI-enhanced version with Google Gemini
├── requirements.txt    # Dependencies
└── .env               # API keys (you create this)
```

## 🛠️ Quick Start

### Step 1: Install Dependencies
```bash
cd chicago_travel_agent
pip install -r requirements.txt
```

### Step 2: Get Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (starts with `AIza`)

### Step 3: Configure API Key
**Option A:** Create `.env` file:
```bash
echo "GEMINI_API_KEY=AIza-your-key-here" > .env
```

**Option B:** Set environment variable:
```bash
export GEMINI_API_KEY="AIza-your-key-here"
```

### Step 4: Run the App
```bash
streamlit run app_v2.py  # AI version
streamlit run app.py      # Basic version
```

## 🔧 Configuration

### Required
- **Google Gemini API Key**: Required for AI-powered recommendations in `app_v2.py`
  - Get one at: https://makersuite.google.com/app/apikey (FREE tier available!)
  - Cost: FREE tier includes 60 requests/minute

### Optional
- **Chicago Data Portal API Key**: For real-time transit data (not currently used in simplified version)

### Environment Variables
Create a `.env` file:
```bash
GEMINI_API_KEY=AIza-your-api-key-here
```

## 🎨 Usage

### AI Version (app_v2.py)
1. **Style Matching Tab**: Select style preferences manually
2. **AI Semantic Search Tab**: 
   - Describe your ideal hotel in natural language
   - AI understands semantic meaning (not just keywords)
   - GPT generates personalized recommendation text
3. **View Results**: See match scores and AI explanations

### Basic Version (app.py)
- Simple style tag matching
- No API key required
- Works completely offline

## 🧪 Testing & Evaluation

### SMART Metrics

- **Style Accuracy**: 85% match score for user-uploaded images vs recommended hotels
- **Efficiency**: Under 5 conversation turns to find suitable hotels (80% of users)
- **User Study**: Visual helpfulness rated 1-5 by 5 participants

### Running Tests

```bash
# Run evaluation suite
python -m pytest tests/

# Run style matching evaluation
python src/evaluation/evaluate_style_matching.py
```

## 📊 Data Sources

- **Hotel Data**: Sample Chicago hotel dataset with style tags and amenities
- **Neighborhood Data**: Comprehensive Chicago neighborhood guides with vibe descriptions
- **Safety Data**: Crime statistics and safety scores by neighborhood
- **Transit Data**: CTA L stops, bus routes, and walkability scores

## 🔄 Agent Workflow

1. **Style Agent**: Analyzes user image/text to extract style preferences
2. **Safety Agent**: Evaluates neighborhood safety scores
3. **Transit Agent**: Assesses public transportation accessibility
4. **Travel Agent**: Orchestrates all agents and ranks hotels by composite score

## 🚀 Future Enhancements

- Real-time booking integration
- Flight tracking capabilities
- User feedback loop for style preference learning
- Mobile app development
- Multi-city expansion

## 📝 Project Structure

```
chicago_travel_agent/
├── app.py              # Basic rule-based version
├── app_v2.py           # AI-enhanced version (RECOMMENDED)
├── requirements.txt    # Python dependencies
├── .env.example        # Template for API keys
└── README.md           # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is part of SI405 Applied AI course work.

## 🙏 Acknowledgments

- Built with LangGraph for agent orchestration
- Uses CLIP for multimodal vision analysis
- ChromaDB for vector storage and RAG
- Streamlit for the interactive UI
- Chicago Data Portal for transit information
