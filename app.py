import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Netflix Content Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #0e0e0e;
    }
    .stMetric {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e50914;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1a;
        border-radius: 5px;
        padding: 10px 20px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e50914;
    }
    h1, h2, h3 {
        color: #e50914;
    }
    .info-box {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #e50914;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    return df

# Data preprocessing functions
@st.cache_data
def preprocess_data(df):
    # Extract duration as integer for movies
    movies = df[df['type'] == "Movie"].copy()
    movies['duration_int'] = movies['duration'].str.extract('(\d+)').astype(float)
    
    # Extract seasons as integer for TV shows
    tv = df[df['type'] == "TV Show"].copy()
    tv['seasons_int'] = tv['duration'].str.extract('(\d+)').astype(float)
    
    # Explode genres
    genres = df['listed_in'].str.split(', ').explode()
    
    # Explode countries
    countries = df['country'].str.split(', ').explode()
    
    # Explode directors
    directors = df['director'].dropna().str.split(', ').explode()
    
    # Explode actors
    actors = df['cast'].dropna().str.split(', ').explode()
    
    return movies, tv, genres, countries, directors, actors

# Header
st.markdown("<h1 style='text-align: center;'>🎬 Netflix Content Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Comprehensive analysis of Netflix's content library</p>", unsafe_allow_html=True)
st.markdown("---")

# Load data
try:
    df = load_data()
    movies, tv, genres, countries, directors, actors = preprocess_data(df)
    
    # Sidebar filters
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=200)
    st.sidebar.markdown("## 🎯 Filters")
    
    # Year range filter
    year_range = st.sidebar.slider(
        "Select Release Year Range",
        int(df['release_year'].min()),
        int(df['release_year'].max()),
        (int(df['release_year'].min()), int(df['release_year'].max()))
    )
    
    # Content type filter
    content_type = st.sidebar.multiselect(
        "Select Content Type",
        options=df['type'].unique(),
        default=df['type'].unique()
    )
    
    # Rating filter
    rating_filter = st.sidebar.multiselect(
        "Select Rating",
        options=df['rating'].dropna().unique(),
        default=df['rating'].dropna().unique()
    )
    
    # Filter data
    filtered_df = df[
        (df['release_year'] >= year_range[0]) &
        (df['release_year'] <= year_range[1]) &
        (df['type'].isin(content_type)) &
        (df['rating'].isin(rating_filter))
    ]
    
    # Create tabs for different analysis sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Overview", "🎭 Genre Analysis", "🌍 Geographic", 
        "⏱️ Time Trends", "⭐ Ratings", "🎬 Cast & Crew", 
        "📈 Advanced Analytics", "🔮 Insights"
    ])
    
    # TAB 1: OVERVIEW
    with tab1:
        st.header("📊 Content Overview")
        
        # KPIs
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Titles", f"{len(filtered_df):,}")
        with col2:
            st.metric("Movies", f"{len(filtered_df[filtered_df['type']=='Movie']):,}")
        with col3:
            st.metric("TV Shows", f"{len(filtered_df[filtered_df['type']=='TV Show']):,}")
        with col4:
            st.metric("Countries", f"{filtered_df['country'].str.split(', ').explode().nunique():,}")
        with col5:
            st.metric("Unique Genres", f"{filtered_df['listed_in'].str.split(', ').explode().nunique():,}")
        
        st.markdown("---")
        
        # Q1 & Q2: Movies vs TV Shows
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Q1: Movies vs TV Shows Count")
            type_counts = filtered_df['type'].value_counts()
            fig = px.bar(
                x=type_counts.index,
                y=type_counts.values,
                labels={'x': 'Content Type', 'y': 'Count'},
                title="Number of Movies vs TV Shows",
                color=type_counts.index,
                color_discrete_map={'Movie': '#e50914', 'TV Show': '#564d4d'}
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Q2: Percentage Distribution")
            fig = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                title="Movies vs TV Shows Distribution",
                color=type_counts.index,
                color_discrete_map={'Movie': '#e50914', 'TV Show': '#564d4d'}
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Q3: Rating Distribution
        st.subheader("Q3: Content Distribution by Ratings")
        rating_counts = filtered_df['rating'].value_counts().sort_values(ascending=True)
        fig = px.bar(
            x=rating_counts.values,
            y=rating_counts.index,
            orientation='h',
            labels={'x': 'Number of Titles', 'y': 'Rating'},
            title="Distribution of Content Ratings",
            color=rating_counts.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q41: Key Netflix KPIs
        st.subheader("Q41: Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_per_year = filtered_df.groupby('release_year').size().mean()
            st.metric("Avg Content/Year", f"{avg_per_year:.0f}")
        with col2:
            total_genres = filtered_df['listed_in'].str.split(', ').explode().nunique()
            st.metric("Total Genres", total_genres)
        with col3:
            total_countries = filtered_df['country'].str.split(', ').explode().nunique()
            st.metric("Contributing Countries", total_countries)
        with col4:
            total_directors = filtered_df['director'].dropna().str.split(', ').explode().nunique()
            st.metric("Unique Directors", total_directors)
    
    # TAB 2: GENRE ANALYSIS
    with tab2:
        st.header("🎭 Genre Analysis")
        
        filtered_genres = filtered_df['listed_in'].str.split(', ').explode()
        
        # Q4 & Q5: Most Common Genres
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Q4: Most Common Genres on Netflix")
            top_genres = filtered_genres.value_counts().head(15)
            fig = px.bar(
                x=top_genres.values,
                y=top_genres.index,
                orientation='h',
                labels={'x': 'Number of Titles', 'y': 'Genre'},
                title="Top 15 Genres",
                color=top_genres.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Q5: Top Genre")
            top_genre = filtered_genres.value_counts().idxmax()
            top_genre_count = filtered_genres.value_counts().max()
            st.markdown(f"""
            <div class="info-box">
                <h2 style="color: #e50914; margin: 0;">{top_genre}</h2>
                <p style="font-size: 24px; margin: 10px 0;">{top_genre_count} titles</p>
                <p style="color: #888;">Most dominant genre on Netflix</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Q20: Least Represented Genre")
            least_genre = filtered_genres.value_counts().tail(1)
            st.markdown(f"""
            <div class="info-box">
                <h3 style="color: #564d4d; margin: 0;">{least_genre.index[0]}</h3>
                <p style="font-size: 20px; margin: 10px 0;">{least_genre.values[0]} titles</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Q16 & Q17: Genre popularity by type
        st.subheader("Q16 & Q17: Genre Popularity by Content Type")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Popular Genres in Movies**")
            movie_genres = filtered_df[filtered_df['type']=="Movie"]['listed_in'].str.split(', ').explode()
            top_movie_genres = movie_genres.value_counts().head(10)
            fig = px.bar(
                x=top_movie_genres.values,
                y=top_movie_genres.index,
                orientation='h',
                color=top_movie_genres.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Popular Genres in TV Shows**")
            tv_genres = filtered_df[filtered_df['type']=="TV Show"]['listed_in'].str.split(', ').explode()
            top_tv_genres = tv_genres.value_counts().head(10)
            fig = px.bar(
                x=top_tv_genres.values,
                y=top_tv_genres.index,
                orientation='h',
                color=top_tv_genres.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Q18: Overall Genre Distribution (Treemap)
        st.subheader("Q18: Overall Genre Distribution (Hierarchical View)")
        top_15_genres = filtered_genres.value_counts().head(15)
        fig = px.treemap(
            names=top_15_genres.index,
            parents=[""] * len(top_15_genres),
            values=top_15_genres.values,
            title="Genre Distribution Treemap"
        )
        fig.update_traces(marker=dict(colorscale='Reds'))
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q19: Genre Evolution Over Time
        st.subheader("Q19: How Genres Have Evolved Over Time")
        genre_year = filtered_df.assign(genre=filtered_df['listed_in'].str.split(', ')).explode('genre')
        genre_year_count = genre_year.groupby(['release_year', 'genre']).size().reset_index(name='count')
        
        top_5_genres = filtered_genres.value_counts().head(5).index
        genre_year_filtered = genre_year_count[genre_year_count['genre'].isin(top_5_genres)]
        
        fig = px.line(
            genre_year_filtered,
            x='release_year',
            y='count',
            color='genre',
            title="Evolution of Top 5 Genres Over Time",
            labels={'release_year': 'Year', 'count': 'Number of Titles'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q47: Genre Dominance
        st.subheader("Q47: Which Genre Dominates Netflix?")
        dominant_genre = filtered_genres.value_counts().head(1)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align: center; background-color: #1a1a1a; padding: 30px; border-radius: 10px;">
                <h1 style="color: #e50914; font-size: 48px; margin: 0;">{dominant_genre.index[0]}</h1>
                <p style="font-size: 32px; color: white; margin: 10px 0;">{dominant_genre.values[0]} titles</p>
                <p style="color: #888; font-size: 18px;">Clear market leader</p>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 3: GEOGRAPHIC ANALYSIS
    with tab3:
        st.header("🌍 Geographic Distribution")
        
        filtered_countries = filtered_df['country'].str.split(', ').explode()
        
        # Q11 & Q14: Country Distribution
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Q11: Top Content-Producing Countries")
            top_countries = filtered_countries.value_counts().head(15)
            fig = px.bar(
                x=top_countries.values,
                y=top_countries.index,
                orientation='h',
                labels={'x': 'Number of Titles', 'y': 'Country'},
                title="Top 15 Countries by Content Production",
                color=top_countries.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Q14: Total Countries")
            total_countries = filtered_countries.nunique()
            st.markdown(f"""
            <div class="info-box">
                <h1 style="color: #e50914; font-size: 48px; margin: 0;">{total_countries}</h1>
                <p style="font-size: 20px; margin: 10px 0;">Countries Contributing</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Q15: Least Contributing Country")
            least_country = filtered_countries.value_counts().tail(1)
            st.markdown(f"""
            <div class="info-box">
                <h3 style="color: #564d4d;">{least_country.index[0]}</h3>
                <p>{least_country.values[0]} title(s)</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Q12: Country-wise Distribution (Pie)
        st.subheader("Q12: Top 5 Countries Distribution")
        top_5_countries = filtered_countries.value_counts().head(5)
        fig = px.pie(
            values=top_5_countries.values,
            names=top_5_countries.index,
            title="Top 5 Content-Producing Countries"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q13: Movies vs TV Shows by Country
        st.subheader("Q13: Content Type Distribution by Country")
        country_type_df = filtered_df.copy()
        country_type_df = country_type_df[country_type_df['country'].notna()]
        country_type_df['country_first'] = country_type_df['country'].str.split(',').str[0].str.strip()
        top_10_countries_list = country_type_df['country_first'].value_counts().head(10).index
        country_type_filtered = country_type_df[country_type_df['country_first'].isin(top_10_countries_list)]
        
        fig = px.histogram(
            country_type_filtered,
            x='country_first',
            color='type',
            barmode='group',
            title="Movies vs TV Shows by Top 10 Countries",
            labels={'country_first': 'Country', 'count': 'Number of Titles'},
            color_discrete_map={'Movie': '#e50914', 'TV Show': '#564d4d'}
        )
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q37: International Content Growth
        st.subheader("Q37: International Content Growth Over Time")
        country_year = filtered_df[filtered_df['country'].notna()].copy()
        country_year['country_first'] = country_year['country'].str.split(',').str[0].str.strip()
        top_countries_for_trend = country_year['country_first'].value_counts().head(5).index
        country_year_filtered = country_year[country_year['country_first'].isin(top_countries_for_trend)]
        country_trend = country_year_filtered.groupby(['release_year', 'country_first']).size().reset_index(name='count')
        
        fig = px.line(
            country_trend,
            x='release_year',
            y='count',
            color='country_first',
            title="Content Growth by Top 5 Countries",
            labels={'release_year': 'Year', 'count': 'Number of Titles', 'country_first': 'Country'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 4: TIME TRENDS
    with tab4:
        st.header("⏱️ Time-Based Trends")
        
        # Q6 & Q9: Releases per year
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Q6: Titles Released Each Year")
            yearly_releases = filtered_df.groupby('release_year').size()
            fig = px.line(
                x=yearly_releases.index,
                y=yearly_releases.values,
                labels={'x': 'Year', 'y': 'Number of Titles'},
                title="Content Releases Per Year",
                markers=True
            )
            fig.update_traces(line_color='#e50914')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Q9: Peak Release Year")
            peak_year = filtered_df['release_year'].value_counts().idxmax()
            peak_count = filtered_df['release_year'].value_counts().max()
            st.markdown(f"""
            <div class="info-box">
                <h1 style="color: #e50914; font-size: 48px; margin: 0;">{peak_year}</h1>
                <p style="font-size: 24px; margin: 10px 0;">{peak_count} releases</p>
                <p style="color: #888;">Most productive year</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Q7: Content Growth Over Time
        st.subheader("Q7: Netflix Content Growth (Cumulative)")
        fig = px.area(
            x=yearly_releases.index,
            y=yearly_releases.values,
            labels={'x': 'Year', 'y': 'Number of Titles'},
            title="Netflix Content Growth Over Time"
        )
        fig.update_traces(fillcolor='rgba(229, 9, 20, 0.3)', line_color='#e50914')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q8: Movies vs TV Shows Per Year
        st.subheader("Q8: Movies vs TV Shows Released Per Year")
        fig = px.histogram(
            filtered_df,
            x='release_year',
            color='type',
            barmode='group',
            title="Content Type Distribution Over Years",
            labels={'release_year': 'Year', 'count': 'Number of Titles'},
            color_discrete_map={'Movie': '#e50914', 'TV Show': '#564d4d'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q10: Content Trend After 2015
        st.subheader("Q10: Content Addition Trend After 2015")
        post_2015 = filtered_df[filtered_df['release_year'] >= 2015].groupby('release_year').size()
        fig = px.line(
            x=post_2015.index,
            y=post_2015.values,
            labels={'x': 'Year', 'y': 'Number of Titles'},
            title="Content Growth from 2015 Onwards",
            markers=True
        )
        fig.update_traces(line_color='#e50914', marker=dict(size=10))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q36: Before vs After 2015
        st.subheader("Q36: Netflix Content - Before vs After 2015")
        period_split = filtered_df['release_year'].apply(lambda x: "Before 2015" if x < 2015 else "2015 and After")
        period_counts = period_split.value_counts()
        
        fig = px.bar(
            x=period_counts.index,
            y=period_counts.values,
            labels={'x': 'Period', 'y': 'Number of Titles'},
            title="Content Distribution: Before vs After 2015",
            color=period_counts.index,
            color_discrete_map={'Before 2015': '#564d4d', '2015 and After': '#e50914'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q39 & Q49: Growth Rate Analysis
        st.subheader("Q39 & Q49: Movies vs TV Shows Growth Rate")
        growth_data = filtered_df.groupby(['release_year', 'type']).size().unstack(fill_value=0)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=growth_data.index, y=growth_data.get('Movie', []), 
                                mode='lines+markers', name='Movies', line=dict(color='#e50914')))
        fig.add_trace(go.Scatter(x=growth_data.index, y=growth_data.get('TV Show', []), 
                                mode='lines+markers', name='TV Shows', line=dict(color='#564d4d')))
        fig.update_layout(title="Movies vs TV Shows Growth Comparison", 
                         xaxis_title="Year", yaxis_title="Number of Titles", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q40 & Q48: Content Diversity
        st.subheader("Q40 & Q48: Genre Diversity by Year")
        diversity = filtered_df.groupby('release_year')['listed_in'].apply(
            lambda x: x.str.split(', ').explode().nunique()
        )
        most_diverse_year = diversity.idxmax()
        
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.line(
                x=diversity.index,
                y=diversity.values,
                labels={'x': 'Year', 'y': 'Number of Unique Genres'},
                title="Genre Diversity Evolution",
                markers=True
            )
            fig.update_traces(line_color='#e50914')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-box">
                <h3 style="color: #e50914;">Most Diverse Year</h3>
                <h1 style="font-size: 48px; margin: 10px 0;">{most_diverse_year}</h1>
                <p style="font-size: 20px;">{diversity.max()} unique genres</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Q42: Average Content Per Year
        st.subheader("Q42: Average Content Added Per Year")
        avg_content = filtered_df.groupby('release_year').size().mean()
        st.markdown(f"""
        <div class="info-box">
            <h2 style="color: #e50914;">Average Releases Per Year</h2>
            <h1 style="font-size: 42px; margin: 10px 0;">{avg_content:.0f}</h1>
            <p style="color: #888;">titles per year on average</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Q43: Total Genres
        st.subheader("Q43: Total Genres on Netflix")
        total_genres = filtered_df['listed_in'].str.split(', ').explode().nunique()
        st.markdown(f"""
        <div class="info-box">
            <h1 style="color: #e50914; font-size: 48px; margin: 0;">{total_genres}</h1>
            <p style="font-size: 20px; margin: 10px 0;">Unique Genres Available</p>
        </div>
        """, unsafe_allow_html=True)
    
    # TAB 5: RATINGS ANALYSIS
    with tab5:
        st.header("⭐ Content Ratings Analysis")
        
        # Q21: Most Common Rating
        st.subheader("Q21: Most Common Rating on Netflix")
        most_common_rating = filtered_df['rating'].value_counts().idxmax()
        rating_count = filtered_df['rating'].value_counts().max()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align: center; background-color: #1a1a1a; padding: 30px; border-radius: 10px;">
                <h1 style="color: #e50914; font-size: 48px; margin: 0;">{most_common_rating}</h1>
                <p style="font-size: 24px; margin: 10px 0;">{rating_count} titles</p>
                <p style="color: #888;">Most prevalent rating</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Q22: Rating Distribution by Type
        st.subheader("Q22: Rating Distribution - Movies vs TV Shows")
        fig = px.histogram(
            filtered_df,
            x='rating',
            color='type',
            barmode='group',
            title="Rating Distribution by Content Type",
            color_discrete_map={'Movie': '#e50914', 'TV Show': '#564d4d'}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q23: Adult Content by Genre
        st.subheader("Q23: Genres with Most Adult-Rated Content (TV-MA)")
        adult_content = filtered_df[filtered_df['rating'] == "TV-MA"]
        if len(adult_content) > 0:
            adult_genres = adult_content['listed_in'].str.split(', ').explode().value_counts().head(10)
            fig = px.bar(
                x=adult_genres.values,
                y=adult_genres.index,
                orientation='h',
                labels={'x': 'Number of Titles', 'y': 'Genre'},
                title="Top Genres in TV-MA Rated Content",
                color=adult_genres.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Q24: Adult vs Family Content
        st.subheader("Q24: Netflix Focus - Adult vs Family Content")
        rating_categories = filtered_df['rating'].value_counts()
        adult_ratings = ['TV-MA', 'R', 'NC-17']
        family_ratings = ['TV-Y', 'TV-Y7', 'TV-G', 'G', 'PG', 'TV-PG']
        
        adult_count = rating_categories[rating_categories.index.isin(adult_ratings)].sum()
        family_count = rating_categories[rating_categories.index.isin(family_ratings)].sum()
        
        fig = px.pie(
            values=[adult_count, family_count],
            names=['Adult Content', 'Family Content'],
            title="Adult vs Family Content Distribution",
            color_discrete_sequence=['#e50914', '#564d4d']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q25: Rating Differences Between Types
        st.subheader("Q25: Rating Distribution Comparison")
        
        # Create a heatmap of ratings by type
        rating_type_pivot = filtered_df.groupby(['type', 'rating']).size().unstack(fill_value=0)
        
        fig = px.imshow(
            rating_type_pivot,
            labels=dict(x="Rating", y="Content Type", color="Count"),
            title="Rating Distribution Heatmap",
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q44: Relationship between Rating and Genre
        st.subheader("Q44: Rating vs Genre Relationship")
        
        # Get top 10 genres
        top_10_genres = filtered_df['listed_in'].str.split(', ').explode().value_counts().head(10).index
        genre_rating_df = filtered_df[filtered_df['listed_in'].str.contains('|'.join(top_10_genres), na=False)]
        genre_rating_df['primary_genre'] = genre_rating_df['listed_in'].str.split(',').str[0]
        
        fig = px.histogram(
            genre_rating_df,
            x='primary_genre',
            color='rating',
            title="Rating Distribution Across Top Genres",
            barmode='stack'
        )
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 6: CAST & CREW
    with tab6:
        st.header("🎬 Cast & Crew Analysis")
        
        filtered_directors = filtered_df['director'].dropna().str.split(', ').explode()
        filtered_actors = filtered_df['cast'].dropna().str.split(', ').explode()
        
        # Q31: Most Prolific Directors
        st.subheader("Q31: Directors with Most Titles")
        top_directors = filtered_directors.value_counts().head(15)
        fig = px.bar(
            x=top_directors.values,
            y=top_directors.index,
            orientation='h',
            labels={'x': 'Number of Titles', 'y': 'Director'},
            title="Top 15 Directors on Netflix",
            color=top_directors.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q32: Most Frequent Actors
        st.subheader("Q32: Most Frequent Actors on Netflix")
        top_actors = filtered_actors.value_counts().head(15)
        fig = px.bar(
            x=top_actors.values,
            y=top_actors.index,
            orientation='h',
            labels={'x': 'Number of Titles', 'y': 'Actor'},
            title="Top 15 Actors on Netflix",
            color=top_actors.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Q33: Multiple Directors
        st.subheader("Q33: Collaborative Productions")
        multiple_directors = filtered_df[filtered_df['director'].str.contains(',', na=False)].shape[0]
        total_with_directors = filtered_df['director'].notna().sum()
        collab_percentage = (multiple_directors / total_with_directors * 100) if total_with_directors > 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <h3 style="color: #e50914;">Titles with Multiple Directors</h3>
                <h1 style="font-size: 48px; margin: 10px 0;">{multiple_directors}</h1>
                <p style="font-size: 20px;">{collab_percentage:.1f}% of titled content</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Q35: Directors Working in Multiple Genres
        with col2:
            st.subheader("Q35: Most Versatile Directors")
            director_genre_diversity = filtered_df.groupby('director')['listed_in'].apply(
                lambda x: x.str.split(', ').explode().nunique()
            ).sort_values(ascending=False).head(5)
            
            for director, genre_count in director_genre_diversity.items():
                if pd.notna(director):
                    st.markdown(f"""
                    <div style="background-color: #1a1a1a; padding: 10px; margin: 5px 0; border-radius: 5px;">
                        <strong>{director}</strong><br>
                        <span style="color: #e50914;">{genre_count} genres</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Q26-Q30: Duration Analysis
        st.header("Duration Analysis")
        
        filtered_movies = filtered_df[filtered_df['type'] == "Movie"].copy()
        filtered_movies['duration_int'] = filtered_movies['duration'].str.extract('(\d+)').astype(float)
        
        filtered_tv = filtered_df[filtered_df['type'] == "TV Show"].copy()
        filtered_tv['seasons_int'] = filtered_tv['duration'].str.extract('(\d+)').astype(float)
        
        # Q26 & Q27: Movie Duration
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Q26: Distribution of Movie Durations")
            fig = px.histogram(
                filtered_movies,
                x='duration_int',
                nbins=30,
                labels={'duration_int': 'Duration (minutes)', 'count': 'Number of Movies'},
                title="Movie Duration Distribution"
            )
            fig.update_traces(marker_color='#e50914')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Q27: Average Movie Duration")
            avg_duration = filtered_movies['duration_int'].mean()
            st.markdown(f"""
            <div class="info-box">
                <h1 style="color: #e50914; font-size: 48px; margin: 0;">{avg_duration:.0f}</h1>
                <p style="font-size: 24px; margin: 10px 0;">minutes</p>
                <p style="color: #888;">Average movie length</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Q29: Most Common Duration")
            mode_duration = filtered_movies['duration_int'].mode()
            if len(mode_duration) > 0:
                st.markdown(f"""
                <div class="info-box">
                    <h2 style="color: #e50914;">{mode_duration.values[0]:.0f} minutes</h2>
                    <p>Most common movie length</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Q28: TV Shows with Multiple Seasons
        st.subheader("Q28: TV Shows with More Than 3 Seasons")
        long_shows = filtered_tv[filtered_tv['seasons_int'] > 3].shape[0]
        total_shows = len(filtered_tv)
        percentage = (long_shows / total_shows * 100) if total_shows > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown(f"""
            <div class="info-box" style="text-align: center;">
                <h1 style="color: #e50914; font-size: 48px; margin: 0;">{long_shows}</h1>
                <p style="font-size: 20px; margin: 10px 0;">TV Shows</p>
                <p style="color: #888;">{percentage:.1f}% have 3+ seasons</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Q30: Movie Duration Trends
        st.subheader("Q30: Movie Duration Trends Over Time")
        if len(filtered_movies) > 0:
            fig = px.scatter(
                filtered_movies,
                x='release_year',
                y='duration_int',
                trendline="lowess",
                labels={'release_year': 'Release Year', 'duration_int': 'Duration (minutes)'},
                title="Are Newer Movies Longer or Shorter?",
                opacity=0.5
            )
            fig.update_traces(marker=dict(color='#e50914', size=5))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 7: ADVANCED ANALYTICS
    with tab7:
        st.header("📈 Advanced Analytics")
        
        # Q45: Rating vs Duration Patterns
        st.subheader("Q45: Rating vs Duration Relationship")
        filtered_movies_rating = filtered_df[filtered_df['type'] == "Movie"].copy()
        filtered_movies_rating['duration_int'] = filtered_movies_rating['duration'].str.extract('(\d+)').astype(float)
        
        if len(filtered_movies_rating) > 0:
            fig = px.scatter(
                filtered_movies_rating,
                x='duration_int',
                y='rating',
                color='rating',
                labels={'duration_int': 'Duration (minutes)', 'rating': 'Rating'},
                title="Movie Duration vs Rating",
                opacity=0.6
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Q46: Correlation between Year and Duration
        st.subheader("Q46: Release Year vs Duration Correlation")
        if len(filtered_movies_rating) > 0:
            correlation = filtered_movies_rating[['release_year', 'duration_int']].corr().iloc[0, 1]
            
            col1, col2 = st.columns([2, 1])
            with col1:
                fig = px.scatter(
                    filtered_movies_rating,
                    x='release_year',
                    y='duration_int',
                    trendline="ols",
                    labels={'release_year': 'Release Year', 'duration_int': 'Duration (minutes)'},
                    title="Correlation Between Release Year and Duration"
                )
                fig.update_traces(marker=dict(color='#e50914', size=5))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f"""
                <div class="info-box">
                    <h3 style="color: #e50914;">Correlation Coefficient</h3>
                    <h1 style="font-size: 48px; margin: 10px 0;">{correlation:.3f}</h1>
                    <p style="color: #888;">
                        {"Positive" if correlation > 0 else "Negative"} correlation<br>
                        {"Movies getting longer" if correlation > 0 else "Movies getting shorter"}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Q38 & Q80: Genre Trends
        st.subheader("Q38 & Q80: Declining Genres")
        
        genre_year = filtered_df.assign(genre=filtered_df['listed_in'].str.split(', ')).explode('genre')
        genre_year_count = genre_year.groupby(['release_year', 'genre']).size().reset_index(name='count')
        
        # Calculate trend for each genre
        genre_trends = {}
        for genre in genre_year_count['genre'].unique():
            genre_data = genre_year_count[genre_year_count['genre'] == genre]
            if len(genre_data) > 1:
                recent_avg = genre_data[genre_data['release_year'] >= genre_data['release_year'].quantile(0.75)]['count'].mean()
                old_avg = genre_data[genre_data['release_year'] <= genre_data['release_year'].quantile(0.25)]['count'].mean()
                if old_avg > 0:
                    genre_trends[genre] = (recent_avg - old_avg) / old_avg
        
        declining_genres = sorted(genre_trends.items(), key=lambda x: x[1])[:10]
        
        if declining_genres:
            fig = px.bar(
                x=[g[1]*100 for g in declining_genres],
                y=[g[0] for g in declining_genres],
                orientation='h',
                labels={'x': 'Change (%)', 'y': 'Genre'},
                title="Top 10 Declining Genres (% Change)",
                color=[g[1] for g in declining_genres],
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Q50: Future Trends Prediction
        st.subheader("Q50: Predicting Future Netflix Trends")
        
        st.markdown("""
        <div class="info-box">
            <h3 style="color: #e50914;">Key Insights for Future Trends</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Growth by content type
        recent_years = filtered_df[filtered_df['release_year'] >= filtered_df['release_year'].max() - 5]
        type_growth = recent_years['type'].value_counts()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Recent Content Type Distribution (Last 5 Years)**")
            fig = px.pie(
                values=type_growth.values,
                names=type_growth.index,
                color_discrete_map={'Movie': '#e50914', 'TV Show': '#564d4d'}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Top Growing Genres**")
            growing_genres = sorted(genre_trends.items(), key=lambda x: x[1], reverse=True)[:5]
            for genre, growth in growing_genres:
                st.markdown(f"""
                <div style="background-color: #1a1a1a; padding: 10px; margin: 5px 0; border-radius: 5px;">
                    <strong>{genre}</strong><br>
                    <span style="color: #e50914;">+{growth*100:.1f}% growth</span>
                </div>
                """, unsafe_allow_html=True)
    
    # TAB 8: KEY INSIGHTS
    with tab8:
        st.header("🔮 Key Insights & Summary")
        
        st.markdown("""
        <div class="info-box">
            <h2 style="color: #e50914;">📊 Executive Summary</h2>
            <p>Comprehensive analysis of Netflix's content library reveals key patterns and trends.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create insight cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎬 Content Composition")
            movie_pct = (len(filtered_df[filtered_df['type']=='Movie']) / len(filtered_df) * 100)
            st.markdown(f"""
            <div class="info-box">
                <ul>
                    <li><strong>{movie_pct:.1f}%</strong> Movies vs <strong>{100-movie_pct:.1f}%</strong> TV Shows</li>
                    <li>Most common rating: <strong>{filtered_df['rating'].value_counts().idxmax()}</strong></li>
                    <li>Average movie duration: <strong>{filtered_movies['duration_int'].mean():.0f} minutes</strong></li>
                    <li>Peak release year: <strong>{filtered_df['release_year'].value_counts().idxmax()}</strong></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🌍 Geographic Reach")
            top_country = filtered_countries.value_counts().idxmax()
            st.markdown(f"""
            <div class="info-box">
                <ul>
                    <li><strong>{filtered_countries.nunique()}</strong> countries contribute content</li>
                    <li>Top producer: <strong>{top_country}</strong></li>
                    <li>International content increasing since 2015</li>
                    <li>Diverse global representation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🎭 Genre Landscape")
            top_genre = filtered_genres.value_counts().idxmax()
            st.markdown(f"""
            <div class="info-box">
                <ul>
                    <li><strong>{filtered_genres.nunique()}</strong> unique genres</li>
                    <li>Dominant genre: <strong>{top_genre}</strong></li>
                    <li>Genre diversity increasing over time</li>
                    <li>Different preferences for Movies vs TV Shows</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📈 Growth Trends")
            st.markdown(f"""
            <div class="info-box">
                <ul>
                    <li>Steady content growth over the years</li>
                    <li>Significant expansion post-2015</li>
                    <li>TV Shows gaining market share</li>
                    <li>Focus on adult-oriented content (TV-MA)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Final recommendations
        st.markdown("---")
        st.markdown("### 💡 Strategic Insights")
        
        insights_col1, insights_col2, insights_col3 = st.columns(3)
        
        with insights_col1:
            st.markdown("""
            <div class="info-box">
                <h4 style="color: #e50914;">Content Strategy</h4>
                <p>• Focus on international markets<br>
                • Maintain genre diversity<br>
                • Balance Movies and TV Shows<br>
                • Continue adult content focus</p>
            </div>
            """, unsafe_allow_html=True)
        
        with insights_col2:
            st.markdown("""
            <div class="info-box">
                <h4 style="color: #e50914;">Market Opportunities</h4>
                <p>• Expand underrepresented genres<br>
                • Target emerging markets<br>
                • Invest in original content<br>
                • Leverage trending genres</p>
            </div>
            """, unsafe_allow_html=True)
        
        with insights_col3:
            st.markdown("""
            <div class="info-box">
                <h4 style="color: #e50914;">Future Outlook</h4>
                <p>• TV Show production increasing<br>
                • International content rising<br>
                • Genre evolution continues<br>
                • Quality over quantity focus</p>
            </div>
            """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("⚠️ Netflix dataset not found. Please ensure 'netflix_titles.csv' is in the same directory as this script.")
    st.info("Expected file: netflix_titles.csv")
except Exception as e:
    st.error(f"⚠️ An error occurred: {str(e)}")
    st.info("Please check your data file and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p>🎬 Netflix Content Analytics Dashboard | Built with Streamlit & Plotly</p>
    <p>Data Analysis covering 50+ insights from Netflix's content library</p>
</div>
""", unsafe_allow_html=True)
