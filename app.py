
import streamlit as st

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
    """Calculate how well hotel matches style preferences"""
    if not preferences:
        return 0.5
    
    matches = sum(1 for pref in preferences if pref.lower() in [tag.lower() for tag in hotel["style_tags"]])
    return min(matches / len(preferences), 1.0)

def recommend_hotels(preferences, neighborhood_filter=None, price_filter=None):
    """Generate hotel recommendations"""
    recommendations = []
    
    for hotel in HOTELS:
        # Apply filters
        if neighborhood_filter and hotel["neighborhood"] != neighborhood_filter:
            continue
        if price_filter and hotel["price_range"] != price_filter:
            continue
        
        # Calculate scores
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
    st.title("""
Chicago Personal Travel Agent
A Streamlit app with AI-powered hotel recommendations
Uses OpenAI GPT for personalized suggestions and Sentence Transformers for semantic similarity
""")

    # Sidebar - User Preferences
    with st.sidebar:
        st.header("🎯 Your Preferences")
        
        # Style preferences
        st.subheader("Style Preferences")
        style_options = ["luxury", "boutique", "modern", "historic", "unique", 
                        "cozy", "elegant", "contemporary", "industrial", "artistic",
                        "trendy", "family", "social", "budget"]
        selected_styles = st.multiselect(
            "Select styles you like:",
            style_options,
            default=["modern", "boutique"],
            help="Choose multiple styles to match your preferences"
        )
        
        # Neighborhood
        st.subheader("Neighborhood")
        neighborhood_options = ["Any"] + list(NEIGHBORHOODS.keys())
        selected_neighborhood = st.selectbox(
            "Choose neighborhood:",
            neighborhood_options,
            index=0
        )
        
        # Price range
        st.subheader("Budget")
        price_options = ["Any", "$", "$$", "$$$", "$$$$"]
        selected_price = st.selectbox(
            "Price range:",
            price_options,
            index=0,
            help="$ = Budget, $$$$ = Luxury"
        )
        
        # Search button
        search_clicked = st.button("🔍 Find Hotels", type="primary", use_container_width=True)
    
    # Main content area
    if search_clicked:
        with st.spinner("Finding perfect hotels for you..."):
            # Prepare filters
            neighborhood_filter = None if selected_neighborhood == "Any" else selected_neighborhood
            price_filter = None if selected_price == "Any" else selected_price
            
            # Get recommendations
            results = recommend_hotels(selected_styles, neighborhood_filter, price_filter)
            
            # Display results
            if results:
                st.success(f"Found {len(results)} hotels matching your preferences!")
                
                # Show top 3 recommendations
                st.subheader("🏆 Top Recommendations")
                
                for i, hotel in enumerate(results[:3], 1):
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.markdown(f"### {i}. {hotel['name']}")
                            st.write(f"📍 **Neighborhood:** {hotel['neighborhood']}")
                            st.write(f"💰 **Price:** {hotel['price_range']}")
                            st.write(f"🎨 **Style:** {', '.join(hotel['style_tags'])}")
                            st.caption(hotel['description'])
                        
                        with col2:
                            st.metric("Style Match", f"{hotel['style_match']:.0%}")
                            st.metric("Safety", f"{hotel['safety_score']:.0%}")
                        
                        with col3:
                            st.metric("Transit", f"{hotel['transit_score']:.0%}")
                            st.metric("Overall", f"{hotel['overall_score']:.1%}", delta_color="normal")
                        
                        st.divider()
                
                # Show all other results
                if len(results) > 3:
                    with st.expander(f"📋 See all {len(results)} hotels"):
                        for hotel in results[3:]:
                            st.write(f"**{hotel['name']}** - {hotel['neighborhood']} | {hotel['price_range']} | {hotel['overall_score']:.1%} match")
            else:
                st.warning("No hotels found matching your criteria. Try adjusting your filters.")
    else:
        # Welcome message
        st.info("👈 Set your preferences in the sidebar and click 'Find Hotels' to get recommendations!")
        
        # Show neighborhood info
        st.subheader("📍 Chicago Neighborhoods")
        cols = st.columns(3)
        for i, (name, info) in enumerate(NEIGHBORHOODS.items()):
            with cols[i % 3]:
                with st.expander(name):
                    st.write(info['description'])
                    st.write(f"🛡️ Safety: {info['safety']:.0%}")
                    st.write(f"🚇 Transit: {info['transit']:.0%}")

if __name__ == "__main__":
    main()
