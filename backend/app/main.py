import pandas as pd
import pickle
import os
import nltk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .utils import run_search

# 1. Download NLTK dependencies immediately to a local writable directory
nltk_data_dir = os.path.join("/tmp", "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)
nltk.download('stopwords', download_dir=nltk_data_dir, quiet=True)
nltk.download('punkt', download_dir=nltk_data_dir, quiet=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Serverless Absolute Pathing
ROOT_DIR = os.getcwd()
DATA_PATH = os.path.join(ROOT_DIR, "data", "5000_data_with_tf_idf.csv")
IDF_PATH = os.path.join(ROOT_DIR, "data", "inverse_document_frequency.pkl")

# 3. Global Caching Strategy
_cached_df = None
_cached_idf = None

def get_data():
    global _cached_df, _cached_idf
    if _cached_df is None:
        _cached_df = pd.read_csv(DATA_PATH)
    if _cached_idf is None:
        with open(IDF_PATH, "rb") as f:
            _cached_idf = pickle.load(f)
    return _cached_df, _cached_idf

@app.get("/search")
def search(query: str, k: int = 5):
    try:
        df, idf_matrix = get_data()
        results = run_search(query, df, idf_matrix, k) 
        return results
    except Exception as e:
        return {"error": str(e)}