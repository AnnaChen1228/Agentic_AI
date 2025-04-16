import requests
import json
def get_data(url):
    data = {
        '$limit': 150,
        '$skip': 0,
        'sort': 'pageviewa',
        'asc':1, # 1 for ascending, -1 for descending
        'featured':'true'
    }
    response = requests.get(url,params=data, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        # print(response.text)
        exit(1)

def preprocess_data(data):
    info = []
    exclude_keys = {'ml_infoTitle', 'abstract', 'desc', 'user', 'updatedAt','multiLangDesc'}
    
    for item in data['data']:
        # 先創建 v_data，排除不需要的鍵
        v_data = {k: v for k, v in item['token']['v'].items() if k not in exclude_keys}
        
        info.append({
            'title': item['token']['v'].get('ml_infoTitle', ''),
            'abstract': item['token']['v'].get('abstract', ''),  # 使用 get 方法，當 key 不存在時返回 ''
            'desc': item['token']['v'].get('desc', ''),
            'infoGrade': item['infoGrade'],
            'infoKeywords': item['infoKeywords'],
            'infoCategories': item['infoCategories'],
            'v': v_data,
            'id': item['filename']
        })
    
    return info

def write_json(data, filename):
    with open(filename, 'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    url = "https://api.cosci.tw/new-sim-lang"
    data = get_data(url)
    after_data = preprocess_data(data)
    file_path = 'data/simulation_info.json'
    write_json(after_data, file_path)
    print(f"Data written to {file_path}")
    
if __name__ == "__main__":
    main()