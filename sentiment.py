from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# Read CSV file with no header; assign column names "Professor" and "Reviews"
df = pd.read_csv("cs_prof_reviews.csv", header=None, names=["Professor", "Reviews"], encoding="latin-1")

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Prepare a list to store results
results = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    professor = row["Professor"].strip()
    reviews_string = row["Reviews"]
    if type(reviews_string) is float:
        print(professor)
        continue
    
    # Split the reviews string on '|' delimiter and clean them up
    reviews = [review.strip() for review in reviews_string.split('|') if review.strip()]
    
    scores = []
    for review in reviews:
        sentiment = analyzer.polarity_scores(review)
        compound = sentiment["compound"]

        # Increase weight for negative sentiment
        if compound < 0:
            compound *= 1.5  # Amplify negative impact
            compound = max(compound, -1)  # Ensure it doesn't drop below -1

        scores.append(compound)

    if scores:
        avg_score = sum(scores) / len(scores)
        normalized_score = ((avg_score + 1) / 2) * 5  # Normalize to a 0-5 scale
    else:
        normalized_score = None

    # Append the professor and their rating to the results list
    results.append({
        "Professor": professor,
        "Rating": abs(round(normalized_score, 2)) if normalized_score is not None else "No Data"
    })

# Create a DataFrame for visualization and print the final ratings
ratings_df = pd.DataFrame(results)
ratings_df.to_csv("cs_prof_ratings.csv", index=False)
print(ratings_df)