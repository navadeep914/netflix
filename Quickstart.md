# 🚀 Quick Start Guide - Netflix Dashboard

## Installation (3 Steps)

### Step 1: Install Dependencies
```bash
pip install streamlit pandas plotly numpy
```

### Step 2: Place Your Data File
Make sure `netflix_titles.csv` is in the same folder as `netflix_dashboard.py`

### Step 3: Run the Dashboard
```bash
streamlit run netflix_dashboard.py
```

That's it! The dashboard will open automatically in your browser. 🎉

## 📱 What You'll See

### Main Features:
- **8 Interactive Tabs** covering all aspects of Netflix content
- **50+ Analytical Questions** answered with beautiful visualizations
- **Dynamic Filters** to customize your analysis
- **Real-time Updates** as you change filters

### Navigation:
1. Use the **sidebar** (left) for filters
2. Click **tabs** at the top to switch between sections
3. **Hover** over charts for detailed information
4. **Download** charts using the camera icon

## 🎯 Key Sections

| Tab | What You'll Find |
|-----|------------------|
| 📊 Overview | Total counts, Movies vs TV Shows, Rating distribution |
| 🎭 Genre Analysis | Popular genres, trends, Movie vs TV genre preferences |
| 🌍 Geographic | Country-wise content, international growth |
| ⏱️ Time Trends | Historical patterns, growth rates, peak years |
| ⭐ Ratings | Rating distributions, adult vs family content |
| 🎬 Cast & Crew | Top directors/actors, duration analysis |
| 📈 Advanced Analytics | Correlations, predictions, declining genres |
| 🔮 Insights | Executive summary, strategic recommendations |

## 💡 Pro Tips

1. **Explore Filters**: Try different year ranges and content types
2. **Compare Trends**: Switch between tabs to spot patterns
3. **Export Data**: Use Plotly's download feature on any chart
4. **Full Screen**: Press F11 for immersive experience
5. **Mobile Friendly**: Works on tablets and phones too!

## ❓ Common Issues

**Dashboard won't start?**
- Check if port 8501 is free
- Try: `streamlit run netflix_dashboard.py --server.port 8502`

**Data not loading?**
- Verify `netflix_titles.csv` is in the correct location
- Check file has all required columns

**Slow performance?**
- Dashboard uses caching - first load may be slower
- Subsequent interactions will be faster

## 🎨 Dashboard Features

- ✅ Netflix-themed dark UI with red accents
- ✅ Interactive Plotly charts (zoom, pan, hover)
- ✅ Responsive design for all screen sizes
- ✅ Real-time filtering across all visualizations
- ✅ Metric cards showing key statistics
- ✅ Trend lines and correlation analysis
- ✅ Comprehensive data coverage (50+ questions)

## 📊 Sample Insights You'll Discover

- What percentage of content is Movies vs TV Shows?
- Which country produces the most content?
- What's the most popular genre?
- How has content grown over the years?
- Which directors have the most titles?
- What's trending and what's declining?
- Are movies getting longer or shorter?
- Much more!

## 🔄 Updating Data

To analyze new data:
1. Replace `netflix_titles.csv` with your updated file
2. Refresh the browser (or restart the app)
3. New analysis will be automatically generated

---

**Questions or Issues?** Check the full README.md for detailed documentation.

**Happy Analyzing! 🎬📊**
