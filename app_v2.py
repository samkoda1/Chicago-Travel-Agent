"""
Chicago Personal Travel Agent - AI Enhanced
A Streamlit app with AI-powered hotel recommendations
Uses Google Gemini for personalized suggestions and Sentence Transformers for semantic similarity
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# AI Model Imports
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Initialize Gemini client only if key is available
gemini_model = None
available_models = []
if GEMINI_AVAILABLE and GEMINI_API_KEY:
    try:
        # Configure with REST transport for better compatibility
        genai.configure(
            api_key=GEMINI_API_KEY,
            transport='rest'
        )
        # List available models
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        # Use the first available model
        if available_models:
            gemini_model = genai.GenerativeModel(available_models[0])
        else:
            st.error("No Gemini models available with your API key")
    except Exception as e:
        st.error(f"Error initializing Gemini: {e}")

try:
    from sentence_transformers import SentenceTransformer, util
    EMBEDDINGS_AVAILABLE = True
    # Load lightweight model for semantic similarity
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    embedding_model = None

# Check AI capabilities
AI_ENABLED = GEMINI_AVAILABLE and gemini_model is not None

# Sample hotel data
HOTELS = [
    {
        "name": "The Langham, Chicago",
        "neighborhood": "River North",
        "price_range": "$$$$",
        "style_tags": ["luxury", "elegant", "modern"],
        "safety_score": 0.95,
        "transit_score": 0.88,
        "description": "Luxury hotel with elegant decor and city views"
    },
    {
        "name": "Hotel EMC Chicago",
        "neighborhood": "Streeterville",
        "price_range": "$$$",
        "style_tags": ["boutique", "modern", "contemporary"],
        "safety_score": 0.92,
        "transit_score": 0.85,
        "description": "Modern boutique hotel with contemporary design"
    },
    {
        "name": "The Publishing House",
        "neighborhood": "River West",
        "price_range": "$$",
        "style_tags": ["boutique", "industrial", "unique"],
        "safety_score": 0.85,
        "transit_score": 0.78,
        "description": "Unique hotel in converted publishing building"
    },
    {
        "name": "The Gwen",
        "neighborhood": "River North",
        "price_range": "$$$$",
        "style_tags": ["luxury", "modern", "artistic"],
        "safety_score": 0.94,
        "transit_score": 0.87,
        "description": "Luxury hotel with artistic design elements"
    },
    {
        "name": "Freehand Chicago",
        "neighborhood": "River North",
        "price_range": "$",
        "style_tags": ["budget", "social", "modern"],
        "safety_score": 0.88,
        "transit_score": 0.92,
        "description": "Budget-friendly hotel with social atmosphere"
    },
    {
        "name": "Chicago Athletic Association",
        "neighborhood": "Loop",
        "price_range": "$$$",
        "style_tags": ["historic", "unique", "luxury"],
        "safety_score": 0.90,
        "transit_score": 0.95,
        "description": "Historic athletic club converted to luxury hotel"
    },
    {
        "name": "The Robey",
        "neighborhood": "Wicker Park",
        "price_range": "$$",
        "style_tags": ["boutique", "modern", "trendy"],
        "safety_score": 0.82,
        "transit_score": 0.75,
        "description": "Trendy boutique hotel in historic art deco building"
    },
    {
        "name": "Lincoln Park Hotel",
        "neighborhood": "Lincoln Park",
        "price_range": "$$",
        "style_tags": ["cozy", "classic", "family"],
        "safety_score": 0.96,
        "transit_score": 0.82,
        "description": "Family-friendly hotel near the park and zoo"
    }
]

NEIGHBORHOODS = {
    "River North": {"safety": 0.94, "transit": 0.87, "description": "Upscale area with galleries and restaurants"},
    "Streeterville": {"safety": 0.92, "transit": 0.85, "description": "Lakeside area near Navy Pier"},
    "River West": {"safety": 0.85, "transit": 0.78, "description": "Trendy area with industrial vibe"},
    "Loop": {"safety": 0.88, "transit": 0.95, "description": "Chicago's business district"},
    "Lincoln Park": {"safety": 0.96, "transit": 0.82, "description": "Family-friendly with parks and zoo"},
    "Wicker Park": {"safety": 0.82, "transit": 0.75, "description": "Hip neighborhood with arts and music"}
}

def calculate_style_match(hotel, preferences):
    """Calculate how well hotel matches style preferences using simple string matching"""
    if not preferences:
        return 0.5
    
    matches = sum(1 for pref in preferences if pref.lower() in [tag.lower() for tag in hotel["style_tags"]])
    return min(matches / len(preferences), 1.0)

def calculate_semantic_similarity(hotel, user_description):
    """Use AI embeddings to calculate semantic similarity between hotel and user preferences"""
    if not EMBEDDINGS_AVAILABLE or not user_description:
        return calculate_style_match(hotel, user_description.split()) if user_description else 0.5
    
    try:
        # Create embeddings
        hotel_text = f"{hotel['name']}. {hotel['description']}. Styles: {', '.join(hotel['style_tags'])}. {hotel['neighborhood']}."
        user_text = user_description
        
        hotel_embedding = embedding_model.encode(hotel_text, convert_to_tensor=True)
        user_embedding = embedding_model.encode(user_text, convert_to_tensor=True)
        
        # Calculate cosine similarity
        similarity = util.pytorch_cos_sim(hotel_embedding, user_embedding).item()
        return max(0, similarity)  # Ensure non-negative
    except Exception as e:
        st.error(f"Embedding error: {e}")
        return calculate_style_match(hotel, user_description.split())

def generate_ai_recommendation(user_preferences, top_hotels):
    """Use Google Gemini to generate personalized recommendation text"""
    if not AI_ENABLED or not top_hotels:
        return None
    
    try:
        # Prepare hotel info for the prompt
        hotels_info = "\n\n".join([
            f"Hotel {i+1}: {h['name']}\n"
            f"- Neighborhood: {h['neighborhood']}\n"
            f"- Price: {h['price_range']}\n"
            f"- Style: {', '.join(h['style_tags'])}\n"
            f"- Description: {h['description']}\n"
            f"- Match Score: {h['overall_score']:.1%}"
            for i, h in enumerate(top_hotels[:3])
        ])
        
        prompt = f"""You are a Chicago travel expert. A user is looking for hotels with these preferences:
{user_preferences}

Here are the top 3 matching hotels:
{hotels_info}

Write a friendly, personalized recommendation (2-3 paragraphs) explaining why these hotels match their preferences. Be specific about what makes each hotel special and how it fits their style. Keep it conversational and helpful."""

        response = gemini_model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        st.error(f"AI generation error: {e}")
        return None

def recommend_hotels(preferences, neighborhood_filter=None, price_filter=None, use_semantic=False, user_description=""):
    """Generate hotel recommendations with optional AI-powered semantic matching"""
    recommendations = []
    
    for hotel in HOTELS:
        # Apply filters
        if neighborhood_filter and hotel["neighborhood"] != neighborhood_filter:
            continue
        if price_filter and hotel["price_range"] != price_filter:
            continue
        
        # Calculate style score (use semantic similarity if enabled)
        if use_semantic and user_description:
            style_score = calculate_semantic_similarity(hotel, user_description)
        else:
            style_score = calculate_style_match(hotel, preferences)
        
        overall_score = (style_score * 0.5) + (hotel["safety_score"] * 0.3) + (hotel["transit_score"] * 0.2)
        
        recommendations.append({
            **hotel,
            "style_match": style_score,
            "overall_score": overall_score
        })
    
    # Sort by overall score
    recommendations.sort(key=lambda x: x["overall_score"], reverse=True)
    return recommendations

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Chicago Travel Agent",
        page_icon="🏨",
        layout="wide"
    )
    
    # Header
    st.title("🏨 Chicago Personal Travel Agent")
    st.markdown("AI-powered hotel recommendations for Chicago")
    
    # API Key Setup Check
    if not GEMINI_API_KEY:
        st.warning("⚠️ **Gemini API Key Not Found**")
        st.markdown("""
        To use AI-powered features, you need to add your Gemini API key:
        
        **Step 1:** Get your API key from https://makersuite.google.com/app/apikey
        
        **Step 2:** Create a `.env` file in your project folder with:
        ```
        GEMINI_API_KEY=AIza-your-key-here
        ```
        
        **Step 3:** Restart the app
        
        *The app will still work without the API key, but AI-powered recommendations will be disabled.*
        """)
        st.divider()
    elif GEMINI_API_KEY and not gemini_model and available_models:
        # Show available models for debugging
        with st.expander("🔧 Debug: Available Gemini Models"):
            st.write("Your API key has access to these models:")
            for model in available_models:
                st.code(model)
    
    # Show AI status
    ai_status_col1, ai_status_col2 = st.columns(2)
    with ai_status_col1:
        if AI_ENABLED:
            st.success("🤖 Gemini AI: Active")
        else:
            st.info("🤖 Gemini AI: Inactive")
    with ai_status_col2:
        if EMBEDDINGS_AVAILABLE:
            st.success("🧠 Semantic Embeddings: Active")
        else:
            st.info("🧠 Semantic Embeddings: Inactive")
    
    st.divider()
    
    # Create tabs for different modes
    tab1, tab2, tab3 = st.tabs(["🎯 Style Matching", "🧠 AI Semantic Search", "ℹ️ About"])
    
    with tab1:
        # Traditional style matching (original functionality)
        st.header("Style-Based Hotel Matching")
        st.markdown("Select style preferences and filters to find matching hotels.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            style_options = ["luxury", "boutique", "modern", "historic", "unique", 
                            "cozy", "elegant", "contemporary", "industrial", "artistic",
                            "trendy", "family", "social", "budget"]
            selected_styles = st.multiselect(
                "Style Preferences:",
                style_options,
                default=["modern", "boutique"]
            )
        
        with col2:
            neighborhood_options = ["Any"] + list(NEIGHBORHOODS.keys())
            selected_neighborhood = st.selectbox(
                "Neighborhood:",
                neighborhood_options,
                index=0
            )
        
        with col3:
            price_options = ["Any", "$", "$$", "$$$", "$$$$"]
            selected_price = st.selectbox(
                "Price Range:",
                price_options,
                index=0,
                help="$ = Budget, $$$$ = Luxury"
            )
        
        if st.button("🔍 Find Hotels (Style Match)", type="primary"):
            neighborhood_filter = None if selected_neighborhood == "Any" else selected_neighborhood
            price_filter = None if selected_price == "Any" else selected_price
            
            results = recommend_hotels(selected_styles, neighborhood_filter, price_filter)
            
            if results:
                st.success(f"Found {len(results)} hotels matching your style preferences!")
                
                for i, hotel in enumerate(results[:3], 1):
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.markdown(f"### {i}. {hotel['name']}")
                            st.write(f"📍 {hotel['neighborhood']} | 💰 {hotel['price_range']}")
                            st.write(f"🎨 {', '.join(hotel['style_tags'])}")
                            st.caption(hotel['description'])
                        
                        with col2:
                            st.metric("Style Match", f"{hotel['style_match']:.0%}")
                            st.metric("Safety", f"{hotel['safety_score']:.0%}")
                        
                        with col3:
                            st.metric("Transit", f"{hotel['transit_score']:.0%}")
                            st.metric("Overall", f"{hotel['overall_score']:.1%}")
                        
                        st.divider()
            else:
                st.warning("No hotels found matching your criteria.")
    
    with tab2:
        # AI-powered semantic search
        st.header("AI Semantic Hotel Search")
        st.markdown("Describe your ideal hotel in natural language. Our AI will understand the meaning and find the best matches.")
        
        if not EMBEDDINGS_AVAILABLE:
            st.warning("⚠️ Semantic search requires `sentence-transformers`. Install with: `pip install sentence-transformers`")
        
        user_description = st.text_area(
            "Describe your ideal hotel experience:",
            placeholder="E.g., 'I want a luxurious hotel with artistic design, great views of the city, and elegant decor. Something modern but with classic touches.'",
            height=100
        )
        
        col1, col2 = st.columns([2, 1])
        with col1:
            semantic_price = st.selectbox("Price Range (Optional):", ["Any", "$", "$$", "$$$", "$$$$"], index=0, key="semantic_price")
        with col2:
            semantic_neighborhood = st.selectbox("Neighborhood (Optional):", ["Any"] + list(NEIGHBORHOODS.keys()), index=0, key="semantic_neighborhood")
        
        if st.button("🧠 Find Hotels (AI Semantic Match)", type="primary", disabled=not user_description.strip()):
            with st.spinner("AI is analyzing your preferences..."):
                neighborhood_filter = None if semantic_neighborhood == "Any" else semantic_neighborhood
                price_filter = None if semantic_price == "Any" else semantic_price
                
                results = recommend_hotels(
                    [], 
                    neighborhood_filter, 
                    price_filter, 
                    use_semantic=True, 
                    user_description=user_description
                )
                
                if results:
                    st.success(f"Found {len(results)} hotels semantically matching your description!")
                    
                    # Generate AI recommendation text if OpenAI is available
                    if AI_ENABLED:
                        ai_recommendation = generate_ai_recommendation(user_description, results[:3])
                        if ai_recommendation:
                            with st.expander("🤖 AI Personalized Recommendation", expanded=True):
                                st.markdown(ai_recommendation)
                    
                    # Show results
                    for i, hotel in enumerate(results[:3], 1):
                        with st.container():
                            col1, col2, col3 = st.columns([3, 1, 1])
                            
                            with col1:
                                st.markdown(f"### {i}. {hotel['name']}")
                                st.write(f"📍 {hotel['neighborhood']} | 💰 {hotel['price_range']}")
                                st.write(f"🎨 {', '.join(hotel['style_tags'])}")
                                st.caption(hotel['description'])
                            
                            with col2:
                                st.metric("Semantic Match", f"{hotel['style_match']:.1%}")
                                st.metric("Safety", f"{hotel['safety_score']:.0%}")
                            
                            with col3:
                                st.metric("Transit", f"{hotel['transit_score']:.0%}")
                                st.metric("Overall", f"{hotel['overall_score']:.1%}")
                            
                            st.divider()
                else:
                    st.warning("No hotels found matching your description.")
    
    with tab3:
        # About section
        st.header("About This App")
        
        st.subheader("🤖 AI Models Used")
        st.markdown("""
        This app uses two AI technologies:
        
        1. **Google Gemini**: Generates personalized recommendation text based on your preferences (uses gemini-1.5-flash or gemini-pro)
        2. **Sentence Transformers (all-MiniLM-L6-v2)**: Calculates semantic similarity between your description and hotel features
        """)
        
        st.subheader("📊 How It Works")
        st.markdown("""
        - **Style Matching**: Traditional keyword matching for style tags
        - **Semantic Search**: AI understands natural language descriptions and finds conceptually similar hotels
        - **AI Recommendations**: GPT generates human-like explanations of why hotels match your preferences
        - **Scoring**: Combines style match (50%), safety (30%), and transit accessibility (20%)
        """)
        
        st.subheader("🔧 Setup")
        st.code("""
# Install dependencies
pip install streamlit google-generativeai python-dotenv sentence-transformers

# Create .env file with your Gemini API key
echo "GEMINI_API_KEY=AIza-your-key-here" > .env

# Run the app
streamlit run app_v2.py
        """)
        
        st.subheader("📍 Chicago Neighborhoods")
        for name, info in NEIGHBORHOODS.items():
            with st.expander(name):
                st.write(info['description'])
                st.write(f"🛡️ Safety Score: {info['safety']:.0%}")
                st.write(f"🚇 Transit Score: {info['transit']:.0%}")

if __name__ == "__main__":
    main()
