import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import os

# Load cleaned data
df = pd.read_csv('data/cleaned_movies.csv')

print("Starting EDA & Visualizations...\n")

# Create output folder for images
os.makedirs('visuals', exist_ok=True)

# 1. Top 10 Movies by Popularity
top_popular = df.nlargest(10, 'popularity')

fig1 = px.bar(top_popular, 
              x='popularity', 
              y='title', 
              orientation='h',
              title='Top 10 Most Popular Movies',
              color='vote_average',
              color_continuous_scale='Viridis')
fig1.write_html('visuals/top_popular_movies.html')
fig1.show()

# 2. Rating Distribution
fig2 = px.histogram(df, x='vote_average', 
                    title='Distribution of Movie Ratings',
                    nbins=20,
                    color_discrete_sequence=['#636EFA'])
fig2.write_html('visuals/rating_distribution.html')
fig2.show()

# 3. Genres Analysis (Exploded)
df_genres = df.explode('genres')
genre_counts = df_genres['genres'].value_counts().head(15)

fig3 = px.bar(x=genre_counts.values, 
              y=genre_counts.index,
              orientation='h',
              title='Most Common Genres',
              labels={'x': 'Number of Movies', 'y': 'Genre'})
fig3.write_html('visuals/top_genres.html')
fig3.show()

# 4. Correlation Heatmap
numeric_cols = ['vote_average', 'vote_count', 'popularity', 'budget', 'revenue', 'profit', 'roi', 'year']
corr = df[numeric_cols].corr()

fig4 = px.imshow(corr, 
                 text_auto=True,
                 aspect="auto",
                 title="Correlation Between Features")
fig4.write_html('visuals/correlation_heatmap.html')
fig4.show()

# 5. Word Cloud for Movie Overviews (if you have overview column) or Keywords
all_keywords = ' '.join(df['keywords_str'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='black').generate(all_keywords)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Keywords in Movies')
plt.savefig('visuals/keywords_wordcloud.png')
plt.show()

print("✅ All visualizations saved in 'visuals/' folder!")
print("You can open the .html files in browser for interactive charts.")