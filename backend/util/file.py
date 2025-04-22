import json
import csv
import os
from pathlib import Path
def read_csv(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)
        return list(data)
    
def read_json(filename):
    with open(filename, newline='', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        return data
    
def write_json(data, filename):
    with open(filename, 'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def write_json_keep(data, filename):
    """保持[{}, {}]格式寫入JSON"""
    try:
        # 讀取現有數據或創建新列表
        existing_data = []
        if Path(filename).exists():
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        
        # 添加新數據並寫入
        existing_data.append(data)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
            
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
