from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from dotenv import load_dotenv
import os
import re
import shutil
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.file import read_json

load_dotenv()
embedding = OpenAIEmbeddings(model='text-embedding-3-small', openai_api_key=os.getenv('OPENAI_API_KEY'))
PERSIST_DIR = './statics/chroma_db'
# 定義不同的集合
vectorstores = {
    'global': {},
    'grade': {},
    'category': {}
}

# 建立名稱映射
collection_names_grade = {
    'Grade 1 to Grade 6': 'grade1-6',
    'Grade 7 to Grade 9': 'grade7-9',
    'Grade 10 to Grade 12': 'grade10-12',
    'Undergraduate': 'undergraduate' 
}

collection_names_categories = {
    'Mechanics': 'mechanics',
    'Wave': 'wave',
    'Thermodynamics': 'thermodynamics',
    'Optics': 'optics',
    'Electromagnetism': 'electromagnetism',
    'Modern Physics': 'modern-physics',
    'Chemistry': 'chemistry',
    'Earth Science': 'earth-science',
    'Other': 'other'
}

def create_db():
    try:
        vectorstore = Chroma(
            collection_name="history",
            embedding_function=embedding,
            persist_directory=PERSIST_DIR
        )
        print("Found existing history collection")
    except:
        vectorstore = Chroma.from_documents(
            documents=[],
            embedding=embedding,
            collection_name="history",
            persist_directory=PERSIST_DIR
        )
        print("Created new history collection")
    # 創建全域集合
    try:
        vectorstore = Chroma(
            collection_name="global",
            embedding_function=embedding,
            persist_directory=PERSIST_DIR
        )
        vectorstores['global']['all'] = vectorstore
        print("Found existing global collection")
    except:
        vectorstore = Chroma.from_documents(
            documents=[],
            embedding=embedding,
            collection_name="global",
            persist_directory=PERSIST_DIR
        )
        vectorstores['global']['all'] = vectorstore
        print("Created new global collection")

    # 創建年級集合
    for grade in collection_names_grade.keys():
        try:
            vectorstore = Chroma(
                collection_name=f"grade-{collection_names_grade[grade]}",
                embedding_function=embedding,
                persist_directory=PERSIST_DIR
            )
            vectorstores['grade'][grade] = vectorstore
            print(f"Found existing grade collection: {grade}")
        except:
            vectorstore = Chroma.from_documents(
                documents=[],
                embedding=embedding,
                collection_name=f"grade-{collection_names_grade[grade]}",
                persist_directory=PERSIST_DIR
            )
            vectorstores['grade'][grade] = vectorstore
            print(f"Created new grade collection: {grade}")

    # 創建類別集合
    for category in collection_names_categories:
        try:
            vectorstore = Chroma(
                collection_name=f"category-{collection_names_categories[category]}",
                embedding_function=embedding,
                persist_directory=PERSIST_DIR
            )
            vectorstores['category'][category] = vectorstore
            print(f"Found existing category collection: {category}")
        except:
            vectorstore = Chroma.from_documents(
                documents=[],
                embedding=embedding,
                collection_name=f"category-{collection_names_categories[category]}",
                persist_directory=PERSIST_DIR
            )
            vectorstores['category'][category] = vectorstore
            print(f"Created new category collection: {category}")

def clean_html(raw_html):
    # 移除 HTML 標籤
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    # 移除多餘的空白行和空格
    cleantext = ' '.join([line.strip() for line in cleantext.splitlines() if line.strip()])
    return cleantext

def check_duplicate(content, vectorstore, similarity_threshold=0.95):
    """檢查是否存在重複內容"""
    try:
        results = vectorstore.similarity_search_with_relevance_scores(
            content,
            k=1
        )
        return bool(results and results[0][1] > similarity_threshold)
    except Exception as e:
        print(f"檢查重複時發生錯誤: {str(e)}")
        return False

def add_simulation_to_db(data, vectorstores):
    for simulation_data in data:
        try:
            # 安全地獲取和清理文本
            cleaned_abstract = clean_html(simulation_data.get('abstract', ''))
            cleaned_desc = clean_html(simulation_data.get('desc', ''))
            intro = simulation_data.get('intro', '')
            # 安全地獲取其他字段
            title = simulation_data.get('title', '')
            sim_id = str(simulation_data.get('id', ''))  # 確保 ID 是字符串
            keywords = simulation_data.get('infoKeywords', [])
            categories = simulation_data.get('infoCategories', [])
            grades = simulation_data.get('infoGrade', [])
            variables = simulation_data.get('v', {})

            # 將變數資訊轉換為文字
            variables_text = ""
            for var_name, var_value in variables.items():
                if var_name.endswith('_comment'):
                    base_name = var_name.replace('_comment', '')
                    unit = variables.get(f"{base_name}_unit", '').strip('"')
                    comment = var_value.strip('"')
                    if comment:
                        variables_text += f"Variable: {base_name}"
                        if comment:
                            variables_text += f" - {comment}"
                        if unit:
                            variables_text += f" ({unit})"
                        variables_text += "\n"

            # 準備全域文檔內容
            all_content = f"""
Title: {title}
Introduction: {intro}
Abstract: {cleaned_abstract}
Description: {cleaned_desc}
Keywords: {', '.join(keywords)}
Categories: {', '.join(categories)}
Grade Levels: {', '.join(grades)}
Variables:
{variables_text}
"""
            
            # 基本 metadata
            metadata = {
                'title': str(title),
                'id': str(sim_id)
            }

            # 檢查全域集合是否有重複
            if check_duplicate(all_content, vectorstores['global']['all'],similarity_threshold=1):
                print(f"Skip duplicate content: {title}")
                continue
            
            # 創建全域文檔
            doc_all = Document(
                page_content=all_content,
                metadata=metadata
            )
            
            # 添加到全域集合
            vectorstores['global']['all'].add_documents([doc_all])
            
            # 處理年級集合
            grades_to_add = grades if grades else list(collection_names_grade.keys())
            
            # 年級相關文檔內容
            grade_content = f"""
Title: {title}
Introduction: {intro}
Abstract: {cleaned_abstract}
Description: {cleaned_desc}
Keywords: {', '.join(keywords)}
Categories: {', '.join(categories)}
Variables:
{variables_text}
"""
            
            doc_grade = Document(
                page_content=grade_content,
                metadata=metadata
            )

            for grade in grades_to_add:
                if grade in vectorstores['grade']:
                    # 檢查該年級集合是否有重複
                    if not check_duplicate(grade_content, vectorstores['grade'][grade],similarity_threshold=1):
                        vectorstores['grade'][grade].add_documents([doc_grade])
            
            # 處理類別集合
            categories_to_add = categories if categories else ['Other']
            
            # 類別相關文檔內容
            category_content = f"""
Title: {title}
Introduction: {intro}
Abstract: {cleaned_abstract}
Description: {cleaned_desc}
Keywords: {', '.join(keywords)}
Grade Levels: {', '.join(grades)}
Variables:
{variables_text}
"""            
            doc_category = Document(
                page_content=category_content,
                metadata=metadata
            )

            for category in categories_to_add:
                if category in vectorstores['category']:
                    # 檢查該類別集合是否有重複
                    if not check_duplicate(category_content, vectorstores['category'][category],similarity_threshold=1):
                        vectorstores['category'][category].add_documents([doc_category])
                else:
                    if not check_duplicate(category_content, vectorstores['category']['Other'],similarity_threshold=1):
                        vectorstores['category']['Other'].add_documents([doc_category])
            
        except Exception as e:
            print(f"Error processing data: {str(e)}")
            print(f"Problematic data title: {simulation_data.get('title', 'Unknown')}")
            continue
            
    print("All simulation data has been added to the database.")

def store_history(history_data):
    vectorstore = Chroma(
        collection_name="history",
        embedding_function=embedding,
        persist_directory=PERSIST_DIR
    )
    
    metadata = {
        'title': str(history_data['title']),  
        'id': str(history_data['id'])         
    }
    
    content = f'''{history_data['query']}:\n{history_data['content']}'''
    
    if check_duplicate(content, vectorstore,similarity_threshold=0.8):
        print(f"Skip duplicate content: {metadata['title']}")
        return
    
    doc_all = Document(
        page_content=content,
        metadata=metadata
    )
    
    try:
        vectorstore.add_documents([doc_all])
        print("成功添加新內容")
        return True
    except Exception as e:
        print(f"添加文檔時發生錯誤: {str(e)}")
        return False


def main():
    file_path = './RAG/data/simulation_info_intro.json'
    data = read_json(file_path)
    if os.path.exists(PERSIST_DIR):
        shutil.rmtree(PERSIST_DIR)
    # 初始化向量存儲
    create_db()
    
    # 添加模擬資料
    add_simulation_to_db(data, vectorstores)
    
    # 打印創建的集合資訊
    print("\nCreated Collections:")
    print("Global Collection:", list(vectorstores['global'].keys()))
    print("Grade Collections:", [collection_names_grade[grade] for grade in vectorstores['grade'].keys()])
    print("Category Collections:", [collection_names_categories[category] for category in vectorstores['category'].keys()])

if __name__ == "__main__":
    main()
