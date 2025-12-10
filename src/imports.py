import pdfplumber
import fitz
import json
import re
import nltk
from nltk.corpus import stopwords
def validate_jsonl(jsonl_path):
    with open(jsonl_path,'r',encoding='utf-8') as f:
        for i,line in enumerate(f, 1):
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                print(f"error line {i}:{e}")
                return
    print(f"no problem")