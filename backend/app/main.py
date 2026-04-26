import csv
import pickle
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .utils import run_search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Caching
_cached_data = None
_cached_idf = None

def get_data():
    global _cached_data, _cached_idf
    root = os.getcwd()
    if _cached_data is None:
        path = os.path.join(root, "data", "5000_data_with_tf_idf.csv")
        with open(path, mode='r', encoding='utf-8') as f:
            _cached_data = list(csv.DictReader(f))
    
    if _cached_idf is None:
        path = os.path.join(root, "data", "inverse_document_frequency.pkl")
        with open(path, "rb") as f:
            _cached_idf = pickle.load(f)
            
    return _cached_data, _cached_idf

def get_data():
    global _cached_df, _cached_idf
    if _cached_df is None:
        _cached_df = pd.read_csv(DATA_PATH)
    if _cached_idf is None:
        with open(IDF_PATH, "rb") as f:
            _cached_idf = pickle.load(f)
    return _cached_df, _cached_idf

@app.get("/api/search")
def search(query: str, k: int = 5):
    try:
        data, idf_matrix = get_data()
        return run_search(query, data, idf_matrix, k)
    except Exception as e:
        return {"error": str(e)}