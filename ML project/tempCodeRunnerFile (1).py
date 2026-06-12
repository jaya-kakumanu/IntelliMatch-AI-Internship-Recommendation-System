import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("internship_dataset_cleaned_ready_for_training.csv")
print("Dataset Loaded Successfully!")
print("Total Available Internships:", len(df))
print("Columns:", list(df.columns))
print("------------------------------------------------------")

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_text'])
print("TF-IDF Vectorization Completed!")
print("Shape of TF-IDF Matrix:", tfidf_matrix.shape)
print("------------------------------------------------------")

def recommend_internships(candidate_profile, top_n=5):

    candidate_vec = tfidf.transform([candidate_profile])

    similarity_scores = cosine_similarity(candidate_vec, tfidf_matrix).flatten()

    top_indices = similarity_scores.argsort()[-top_n:][::-1]

    recommendations = df.iloc[top_indices][[
        'internship_id', 'profile', 'company', 'Location',
        'Stipend', 'Duration', 'Skills', 'Education', 'Mode'
    ]].copy()

    recommendations['Similarity_Score'] = similarity_scores[top_indices]

    return recommendations


candidate_profile = input("\n🧍 Enter your profile details (education qualification, skills, role, Duration, Location, Mode,):\n➡️  ")
top_recommendations = recommend_internships(candidate_profile)
print("\n🔍 Top 5 Internship Recommendations:")
print("------------------------------------------------------")
for idx, row in top_recommendations.iterrows():
    print(f"{idx+1}. {row['profile'].title()} at {row['company'].title()}")
    print(f"   📍 Location: {row['Location'].title()} | Mode: {row['Mode']}")
    print(f"   🎯 Skills: {row['Skills']}")
    print(f"   💰 Stipend: {row['Stipend']} | ⏱ Duration: {row['Duration']}")
    print(f"   📈 Similarity Score: {round(row['Similarity_Score'], 3)}")
    print("------------------------------------------------------")

top_recommendations.to_csv("recommended_internships_output.csv", index=False)
print("\nRecommendations saved to 'recommended_internships_output.csv'")
print("------------------------------------------------------")

