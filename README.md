# netflix
# Netflix Content Analytics Dashboard

A comprehensive Streamlit dashboard analyzing Netflix's content library with 50+ insights and beautiful visualizations.

## 🎬 Features

### 8 Interactive Tabs:
1. **📊 Overview** - Content distribution, KPIs, and basic statistics
2. **🎭 Genre Analysis** - Genre trends, popularity, and evolution
3. **🌍 Geographic** - Country-wise content distribution and growth
4. **⏱️ Time Trends** - Historical trends and growth patterns
5. **⭐ Ratings** - Rating distributions and patterns
6. **🎬 Cast & Crew** - Directors, actors, and duration analysis
7. **📈 Advanced Analytics** - Correlations and predictive insights
8. **🔮 Insights** - Executive summary and strategic recommendations

## 📋 Questions Answered

The dashboard answers all 50 questions from your Netflix analysis:

**Content Overview (Q1-Q3)**
- Movies vs TV Shows count and percentage
- Rating distribution

**Genre Analysis (Q4-Q5, Q16-Q20, Q47)**
- Most and least common genres
- Genre trends over time
- Genre dominance

**Geographic Distribution (Q11-Q15, Q37)**
- Top content-producing countries
- International content growth

**Time-Based Trends (Q6-Q10, Q36, Q39-Q40, Q42-Q43, Q48-Q49)**
- Yearly releases and growth
- Content trends before/after 2015
- Genre diversity evolution

**Ratings Analysis (Q21-Q25, Q44)**
- Most common ratings
- Adult vs family content focus
- Rating-genre relationships

**Cast & Crew (Q26-Q35)**
- Top directors and actors
- Movie duration analysis
- TV show seasons
- Director versatility

**Advanced Analytics (Q38, Q45-Q46, Q50, Q80)**
- Duration correlations
- Declining genres
- Future trend predictions

**Key Metrics (Q41)**
- Overall Netflix KPIs

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Required Packages

```bash
pip install streamlit pandas plotly numpy
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Prepare Your Data

Ensure you have the `netflix_titles.csv` file in the same directory as the script. The CSV should contain columns:
- show_id
- type
- title
- director
- cast
- country
- date_added
- release_year
- rating
- duration
- listed_in
- description

## 🎯 Running the Dashboard

### Method 1: Basic Command
```bash
streamlit run netflix_dashboard.py
```

### Method 2: With Custom Port
```bash
streamlit run netflix_dashboard.py --server.port 8501
```

### Method 3: With Custom Configuration
```bash
streamlit run netflix_dashboard.py --server.port 8501 --server.address localhost
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

## 🎨 Features & Interactions

### Interactive Filters (Sidebar)
- **Year Range Slider**: Filter content by release year
- **Content Type**: Select Movies, TV Shows, or both
- **Rating Filter**: Choose specific ratings

### Visualizations
- Bar charts and histograms
- Pie charts for distributions
- Line charts for trends
- Scatter plots for correlations
- Treemaps for hierarchical data
- Heatmaps for patterns
- Area charts for growth

### UI Features
- Netflix-inspired dark theme
- Red (#e50914) accent colors
- Responsive layout
- Metric cards with KPIs
- Information boxes
- Interactive plotly charts (hover, zoom, pan)

## 📊 Data Insights

The dashboard provides insights across multiple dimensions:

1. **Content Composition**: Movies vs TV Shows distribution
2. **Genre Trends**: Popular and declining genres
3. **Geographic Reach**: International content distribution
4. **Temporal Patterns**: Growth over time
5. **Rating Analysis**: Content maturity levels
6. **Creator Analytics**: Top directors and actors
7. **Duration Patterns**: Movie lengths and TV show seasons
8. **Strategic Insights**: Future trend predictions

## 🛠️ Customization

### Changing Colors
Edit the color schemes in the code:
```python
color_discrete_map={'Movie': '#e50914', 'TV Show': '#564d4d'}
```

### Modifying Filters
Adjust sidebar filters in the code:
```python
year_range = st.sidebar.slider(...)
content_type = st.sidebar.multiselect(...)
```

### Adding New Visualizations
Add new plots in any tab section:
```python
fig = px.bar(data, x='column1', y='column2')
st.plotly_chart(fig, use_container_width=True)
```

## 📁 Project Structure

```
.
├── netflix_dashboard.py    # Main dashboard application
├── netflix_titles.csv      # Netflix dataset (required)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Troubleshooting

### Port Already in Use
```bash
streamlit run netflix_dashboard.py --server.port 8502
```

### Data File Not Found
Ensure `netflix_titles.csv` is in the same directory as the script.

### Package Import Errors
Reinstall packages:
```bash
pip install --upgrade streamlit pandas plotly numpy
```

### Performance Issues
For large datasets, the caching decorators (`@st.cache_data`) help optimize performance. If still slow, consider:
- Reducing the data size
- Filtering data before loading
- Simplifying visualizations

## 💡 Tips for Best Experience

1. **Full Screen Mode**: Press F11 for immersive experience
2. **Dark Mode**: Dashboard is optimized for dark theme
3. **Explore Filters**: Try different combinations for unique insights
4. **Interactive Charts**: Hover over charts for detailed information
5. **Download Data**: Use Plotly's built-in download feature on charts

## 📈 Performance

- Data loading is cached for fast reloads
- Preprocessing is optimized
- Responsive design works on various screen sizes
- Smooth interactions with plotly charts

## 🤝 Contributing

Feel free to enhance the dashboard:
- Add new visualizations
- Implement additional filters
- Create new analysis sections
- Improve UI/UX

## 📝 Notes

- The dashboard uses Netflix's brand colors for theming
- All 50 questions from the original analysis are covered
- Charts are interactive and can be downloaded
- Filters apply across all tabs
- Data is cached for performance

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## 📄 License

This dashboard is created for educational and analytical purposes.

---

**Enjoy exploring Netflix's content library! 🎬🍿**
