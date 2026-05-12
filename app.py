import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MovieMind", page_icon="🎬", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {padding: 2rem;}
    h1 {color: #f1c40f;}
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv('data/cleaned_movies.csv')

df = load_data()

# ================== SIDEBAR ==================
st.sidebar.title("🎥 MovieMind")
st.sidebar.markdown("**Discover Movies**")

page = st.sidebar.radio("Navigation", 
    ["🏠 Home", "🔎 Search Movies", "🎭 Genre Explorer", "🏆 Top Movies", "🤖 Recommendations", "📊 Insights", "ℹ️ About"])

# ================== HOME ==================
if page == "🏠 Home":
    st.title("🎬 Welcome to MovieMind")
    st.markdown("### Intelligent Movie Discovery & Recommendation System")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Movies", len(df))
    with col2: st.metric("Avg Rating", round(df['vote_average'].mean(), 2))
    with col3: st.metric("Highest Rated", df['vote_average'].max())
    with col4: st.metric("Most Popular", df.loc[df['popularity'].idxmax(), 'title'][:22])

# ================== SEARCH MOVIES (New Dedicated Page) ==================
elif page == "🔎 Search Movies":
    st.title("🔎 Search Movies")
    
    search_term = st.text_input("Enter Movie Name", placeholder="Type movie title here...", key="search_input")
    
    col1, col2 = st.columns([3,1])
    with col1:
        if st.button("🔍 Search", type="primary"):
            if search_term:
                results = df[df['title'].str.contains(search_term, case=False, na=False)]
                
                if not results.empty:
                    st.success(f"Found **{len(results)}** movies matching '{search_term}'")
                    st.dataframe(results[['title', 'genres_str', 'vote_average', 'popularity', 'year']], 
                               use_container_width=True, hide_index=True)
                else:
                    st.error("No movies found. Try different keywords.")
            else:
                st.warning("Please enter a movie name")

    # Show trending while searching
    st.subheader("Trending Movies")
    trending = df.nlargest(10, 'popularity')
    st.dataframe(trending[['title', 'genres_str', 'vote_average', 'popularity']], 
                use_container_width=True, hide_index=True)

# ================== GENRE EXPLORER ==================
elif page == "🎭 Genre Explorer":
    st.title("🎭 Genre Explorer")
    
    all_genres = set()
    for g in df['genres']:
        try:
            all_genres.update(eval(g) if isinstance(g, str) else g)
        except:
            pass
    
    selected_genres = st.multiselect("Select Genres", sorted(list(all_genres)), default=["Action"])
    sort_by = st.selectbox("Sort By", ["popularity", "vote_average", "success_score"])
    num_movies = st.slider("Number of Results", 5, 30, 15)
    
    if selected_genres:
        mask = df['genres'].apply(lambda x: any(gen in str(x) for gen in selected_genres))
        filtered = df[mask].nlargest(num_movies, sort_by)
        st.dataframe(filtered[['title', 'genres_str', 'vote_average', 'popularity', 'year']], 
                    use_container_width=True, hide_index=True)

# ================== Other Pages (Kept Simple) ==================
elif page == "🏆 Top Movies":
    st.title("🏆 Top Movies")
    metric = st.selectbox("Rank by", ['popularity', 'vote_average'])
    n = st.slider("Show Top", 5, 30, 15)
    top = df.nlargest(n, metric)
    fig = px.bar(top, x=metric, y='title', orientation='h', color='vote_average')
    st.plotly_chart(fig, use_container_width=True)

elif page == "🤖 Recommendations":
    st.title("🤖 Recommendations")
    selected_movie = st.selectbox("Pick a movie you liked", df['title'].unique())
    if st.button("Get Similar Movies", type="primary"):
        movie = df[df['title'] == selected_movie].iloc[0]
        df['similarity'] = df['genres'].apply(
            lambda x: len(set(eval(x)) & set(eval(movie['genres']))) if isinstance(x, str) else 0
        )
        recs = df.nlargest(8, 'similarity')
        st.dataframe(recs[['title', 'genres_str', 'vote_average', 'popularity']], use_container_width=True)

elif page == "📊 Insights":
    st.title("📊 Insights")
    fig = px.scatter(df, x='vote_average', y='popularity', hover_data=['title'], color='year')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.title("About MovieMind")
    st.info("This is a complete portfolio project demonstrating Data Collection, EDA, Visualization, and Recommendation System using TMDb data.")

st.caption("🚀 MovieMind Portfolio Project, Build by Sateesh Kumar Doultani")