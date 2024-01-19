# import spacy
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# try:
#     nlp = spacy.load("en_core_web_sm")
# except OSError:
#     import subprocess
#     subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
#     nlp = spacy.load("en_core_web_sm")


# def extract_text_features(text):
#     # Use spaCy for text feature extraction
#     doc = nlp(text)
#     return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])


# def extract_and_compare(resume_path, job_description):
#     # Extract features from job description
#     job_description_features = extract_text_features(job_description)

#     # Read resume with explicit encoding and error handling
#     with open(resume_path, 'r', encoding='utf-8', errors='ignore') as file:
#         resume_text = file.read()

#     # Extract features from resume
#     resume_features = extract_text_features(resume_text)

#     # TF-IDF Vectorization
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform([job_description_features, resume_features])

#     # Calculate cosine similarity
#     cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

#     print("Cosine Similarity:", cosine_sim)

#     # Identify missing terms from the job description
#     missing_terms = set(job_description_features.split()) - set(resume_features.split())

#     # Adjusted threshold
#     if cosine_sim >= 0.3:  # Experiment with different threshold values
#         suggestions = "Your resume closely matches the job description. No major updates are needed."
#     else:
#         suggestions = f"Your resume may need some updates to align better with the job description. Add details about: {', '.join(missing_terms)}"

#     return suggestions

import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import PyPDF2
import chardet

nlp = spacy.load("en_core_web_md")

def extract_word_embeddings(text):
    doc = nlp(text)
    return doc.vector

def preprocess_text(text):
    # You may need more sophisticated preprocessing based on your data
    return text.lower()  # Convert to lowercase for case-insensitive comparison

def extract_and_compare(resume_path, job_description):
    # Read PDF and replace null characters
    with open(resume_path, 'rb') as file:
        raw_data = file.read()

        # Use chardet to detect the encoding
        result = chardet.detect(raw_data)
        resume_text = raw_data.decode(result['encoding'], errors='replace')

    # Preprocess the text
    job_description = preprocess_text(job_description)
    resume_text = preprocess_text(resume_text)

    # Extract features from job description
    job_description_features = extract_word_embeddings(job_description)

    # Extract features from resume
    resume_features = extract_word_embeddings(resume_text)

    # Calculate cosine similarity
    cosine_sim = np.dot(job_description_features, resume_features) / (
            np.linalg.norm(job_description_features) * np.linalg.norm(resume_features))

    print("Cosine Similarity:", cosine_sim)

    # For embeddings-based similarity, you might need a different approach to identify missing terms

    # Placeholder for missing terms
    missing_terms = []

    # Check for missing terms in the job description
    for term in nlp(job_description):
        if term.text not in nlp(resume_text):
            missing_terms.append(term.text)

    # Adjusted threshold
    if cosine_sim >= 0.5:
        suggestions = "Your resume closely matches the job description. No major updates are needed."
    else:
        suggestions = f"Your resume may need some updates to align better with the job description. Add details about: {', '.join(missing_terms)}"

    return suggestions