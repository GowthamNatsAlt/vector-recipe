import ast
import csv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import os
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
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(os.path.dirname(base_dir), "data")
    
    csv_path = os.path.join(data_dir, "5000_data_with_tf_idf.csv")
    pkl_path = os.path.join(data_dir, "inverse_document_frequency.pkl")
    
    # Check if files exist and load them
    if _cached_data is None:
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV not found at {csv_path}")
            
        with open(csv_path, mode='r', encoding='utf-8') as f:
            # Pre-parsing here as discussed for performance
            raw_data = list(csv.DictReader(f))
            for row in raw_data:
                for col in ['ingredients', 'directions', 'NER', 'tfidf']:
                    if isinstance(row.get(col), str):
                        try:
                            row[col] = ast.literal_eval(row[col])
                        except:
                            row[col] = [] if col != 'tfidf' else {}
            _cached_data = raw_data
    
    # 5. Check if pickle exists and load it
    if _cached_idf is None:
        if not os.path.exists(pkl_path):
            raise FileNotFoundError(f"Pickle not found at {pkl_path}")
            
        with open(pkl_path, "rb") as f:
            _cached_idf = pickle.load(f)
            
    return _cached_data, _cached_idf

@app.get("/api/search")
def search(query: str, k: int = 5):
    try:
        data, idf_matrix = get_data()
        return run_search(query, data, idf_matrix, k)
    except Exception as e:
        return {"error": str(e)}