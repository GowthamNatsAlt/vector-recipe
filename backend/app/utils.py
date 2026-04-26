import csv
import re
import math
import ast
from .stopwords import STOPWORDS

# --- UTILITY FUNCTIONS ---

def clean_data(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\d+/\d+|\d+\.\d+|\d+', '', text)
    noise_list = [
        'lb', 'lbs', 'oz', 'gram', 'grams', 'kg', 'g', 'ml', 'clove', 'cloves', 'c',
        'cup', 'cups', 'tsp', 'teaspoon', 'tbsp', 'tablespoon', 'can', 'pkgs',
        'diced', 'minced', 'chopped', 'sliced', 'shredded', 'grated', 'crushed', 
        'mashed', 'pureed', 'ground', 'slivered', 'halved', 'quartered', 'cubed', 'grnd',
        'frozen', 'chilled', 'melted', 'fresh', 'dried', 'cooked', 'raw', 
        'large', 'small', 'medium', 'optional', 'divided', 'drained', 'rinsed'
    ]
    noise_pattern = r'\b(' + '|'.join(noise_list + list(STOPWORDS)) + r')\b'
    text = re.sub(noise_pattern, '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def remove_stopwords(text: str) -> str:
    return ' '.join([word for word in text.split() if word not in STOPWORDS])

def calculate_term_frequency(text: str) -> dict:
    all_terms = text.split()
    if not all_terms: return {}
    total_terms = len(all_terms)
    term_freq = {}
    for term in all_terms:
        term_freq[term] = term_freq.get(term, 0) + (1/total_terms)
    return term_freq

def calculate_tfidf(dictionary: dict, idf_matrix: dict) -> dict:
    tfidf = {}
    for key, value in dictionary.items():
        tfidf[key] = value * idf_matrix.get(key, 0)
    return tfidf

def process_query(query: str, idf_matrix: dict):
    clean = clean_data(query)
    no_stop = remove_stopwords(clean)
    tf = calculate_term_frequency(no_stop)
    return calculate_tfidf(tf, idf_matrix)

def calculate_magnitude(tfidf_dict: dict) -> float:
    if not tfidf_dict: return 0
    return math.sqrt(sum(value ** 2 for value in tfidf_dict.values()))

def calculate_dot_product(query_vec: dict, recipe_vec: dict) -> float:
    dot_product = 0
    for word, weight in query_vec.items():
        if word in recipe_vec:
            dot_product += recipe_vec[word] * weight
    return dot_product

def get_similarity(query_vec: dict, recipe_vec: dict) -> float:
    dot_product = calculate_dot_product(query_vec, recipe_vec)
    mag_q = calculate_magnitude(query_vec)
    mag_r = calculate_magnitude(recipe_vec)
    if mag_q == 0 or mag_r == 0: return 0
    return dot_product / (mag_q * mag_r)

def run_search(query_str: str, data_list: list, idf_matrix: dict, k: int = 5):
    query_vec = process_query(query_str, idf_matrix)
    if not query_vec: return []
    
    scored_results = []
    for row in data_list:
        score = get_similarity(query_vec, row['tfidf'])
        
        if score > 0:
            result_item = row.copy()
            result_item['score'] = score
            scored_results.append(result_item)

    scored_results.sort(key=lambda x: x['score'], reverse=True)
    return scored_results[:k]