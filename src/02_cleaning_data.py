import pandas as pd
import ast
import numpy as np

# Load the raw data
df = pd.read_csv('data/raw_movies.csv')

print("Original Shape:", df.shape)
print("\nMissing Values:\n", df.isnull().sum())

# ================== Cleaning ==================

# 1. Convert string lists back to actual lists
list_columns = ['genres', 'cast', 'keywords']

for col in list_columns:
    df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# 2. Handle missing values
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['budget'] = df['budget'].replace(0, np.nan)
df['revenue'] = df['revenue'].replace(0, np.nan)

# Fill missing vote_average with median
df['vote_average'] = df['vote_average'].fillna(df['vote_average'].median())

# 3. Create new useful columns
df['genres_str'] = df['genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
df['cast_str'] = df['cast'].apply(lambda x: ', '.join(x[:5]) if isinstance(x, list) else '')  # Top 5 cast
df['keywords_str'] = df['keywords'].apply(lambda x: ', '.join(x[:8]) if isinstance(x, list) else '')

# Profit and ROI
df['profit'] = df['revenue'] - df['budget']
df['roi'] = df.apply(lambda row: row['profit']/row['budget'] if row['budget'] > 0 else np.nan, axis=1)

# Year extraction
df['year'] = df['release_date'].dt.year

# Success score (simple metric)
df['success_score'] = df['vote_average'] * np.log1p(df['vote_count']) * df['popularity']/100

print("\n✅ After Cleaning:")
print("Shape:", df.shape)
print("\nColumns now available:\n", df.columns.tolist())

# Save cleaned data
df.to_csv('data/cleaned_movies.csv', index=False)
print("\n💾 Cleaned data saved as 'data/cleaned_movies.csv'")

# Quick overview
print("\nTop 5 movies by popularity:")
print(df[['title', 'vote_average', 'popularity', 'year']].sort_values('popularity', ascending=False).head())