import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Netflix Data Analysis",
    page_icon="🎬",
    layout="wide"
)

# Title and Introduction
st.title("🎬 Netflix Dataset Analysis")
st.markdown("""
This application visualizes the Netflix catalog, showing the distribution of Movies and TV Shows, 
ratings, and trends over time.
""")

# --- Data Loading ---
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        # Fallback if no file is uploaded yet
        return None
    
    # Basic Preprocessing found in typical Netflix EDA notebooks
    # 1. Handle missing values for critical columns if necessary
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month_name()
    
    return df

# --- Sidebar ---
st.sidebar.header("User Input")
uploaded_file = st.sidebar.file_uploader("Upload your Netflix CSV file", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    # Sidebar Filters
    st.sidebar.subheader("Filters")
    type_filter = st.sidebar.multiselect(
        "Select Content Type",
        options=df['type'].unique(),
        default=df['type'].unique()
    )
    
    # Filter Data
    df_filtered = df[df['type'].isin(type_filter)]

    # --- KPI Row ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Titles", df_filtered.shape[0])
    col2.metric("Movies", df_filtered[df_filtered['type'] == 'Movie'].shape[0])
    col3.metric("TV Shows", df_filtered[df_filtered['type'] == 'TV Show'].shape[0])

    st.markdown("---")

    # --- Visualizations ---
    
    # 1. Distribution of Content Type (Pie Chart)
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Distribution of Content")
        fig_pie = px.pie(
            df_filtered, 
            names='type', 
            title='Movies vs TV Shows',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # 2. Ratings Distribution (Bar Chart)
    with col_chart2:
        st.subheader("Content Ratings Distribution")
        rating_counts = df_filtered['rating'].value_counts().reset_index()
        rating_counts.columns = ['rating', 'count']
        fig_bar = px.bar(
            rating_counts, 
            x='rating', 
            y='count', 
            title='Count of Titles by Rating',
            color='count',
            color_continuous_scale='Redor'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # 3. Content Added Over Years (Line/Area Chart)
    st.subheader("Content Added Over Time")
    if 'year_added' in df_filtered.columns:
        year_counts = df_filtered.groupby(['year_added', 'type']).size().reset_index(name='count')
        fig_line = px.area(
            year_counts, 
            x='year_added', 
            y='count', 
            color='type',
            title='Content Added by Year',
            color_discrete_sequence=['#b20710', '#221f1f'] # Netflix-ish colors
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # 4. Top 10 Countries
    st.subheader("Top 10 Producing Countries")
    # Clean country data (handle movies with multiple countries)
    country_df = df_filtered['country'].dropna().str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
    country_counts = country_df.value_counts().head(10).reset_index()
    country_counts.columns = ['country', 'count']
    
    fig_country = px.bar(
        country_counts, 
        x='count', 
        y='country', 
        orientation='h', 
        title='Top 10 Countries by Content Count',
        color='count',
        color_continuous_scale='Reds'
    )
    fig_country.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_country, use_container_width=True)

    # --- Data View ---
    with st.expander("View Raw Data"):
        st.dataframe(df_filtered)

else:
    st.info("Please upload a CSV file (e.g., netflix_titles.csv) to begin analysis.")
    st.markdown("If you don't have the file, you can download it from Kaggle.")
