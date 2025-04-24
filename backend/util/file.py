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
    
def write_json_rag(data, filename):
    """保持[{}, {}]格式寫入JSON，避免重複數據"""
    try:
        # 讀取現有數據或創建新列表
        existing_data = []
        if Path(filename).exists():
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        
        # 檢查是否已存在相同的數據
        is_duplicate = False
        for existing_item in existing_data:
            if (existing_item.get('query') == data.get('query') and 
                existing_item.get('id') == data.get('id')):
                is_duplicate = True
                break
        
        # 只有不是重複數據時才添加
        if not is_duplicate:
            existing_data.append(data)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)
            
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
