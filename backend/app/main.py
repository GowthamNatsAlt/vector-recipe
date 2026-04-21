# backend/src/main.py
import pandas as pd
import pickle
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .utils import run_search, download_nltk_dependencies

download_nltk_dependencies()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data globally
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../../data/5000_data_with_tf_idf.csv")
IDF_PATH = os.path.join(BASE_DIR, "../../data/inverse_document_frequency.pkl")

df = pd.read_csv(DATA_PATH)
with open(IDF_PATH, "rb") as f:
    idf_matrix = pickle.load(f)

@app.get("/search")
def search(query: str, k: int = 5):
    try:
        results = run_search(query, df, idf_matrix, k) 
        return results
    except Exception as e:
        return {"error": str(e)}