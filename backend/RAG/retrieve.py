from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()
embedding = OpenAIEmbeddings(model='text-embedding-3-small', openai_api_key=os.getenv('OPENAI_API_KEY'))
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5, api_key=os.getenv('OPENAI_API_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
PERSIST_DIR = './statics/chroma_db'



item = {
    1:'global',
    2:'grade',
    3:'category',
}
grade = {
    1: 'Grade 1 to Grade 6',
    2: 'Grade 7 to Grade 9',  
    3: 'Grade 10 to Grade 12',
    4: 'Undergraduate'
}

categories = {
    1: 'Mechanics',
    2: 'Wave',
    3: 'Thermodynamics',
    4: 'Optics',
    5: 'Electromagnetism',
    6: 'Modern Physics',
    7: 'Chemistry',
    8: 'Earth Science',
    9: 'Other'
}

def load_vectorstores():
    vectorstores = {
        'global': {},
        'grade': {},
        'category': {}
    }
    """載入所有向量數據庫"""
    embedding = OpenAIEmbeddings(
        model='text-embedding-3-small', 
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    
    # 載入全域集合
    vectorstores['global']['all'] = Chroma(
        collection_name="global",
        embedding_function=embedding,
        persist_directory='./statics/chroma_db'
    )
    
    # 載入年級集合
    collection_names_grade = {
        'Grade 1 to Grade 6': 'grade1-6',
        'Grade 7 to Grade 9': 'grade7-9',
        'Grade 10 to Grade 12': 'grade10-12',
        'Undergraduate': 'undergraduate'
    }
    
    for grade, collection_name in collection_names_grade.items():
        vectorstores['grade'][grade] = Chroma(
            collection_name=f"grade-{collection_name}",
            embedding_function=embedding,
            persist_directory='./statics/chroma_db'
        )
    
    # 載入類別集合
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
    
    for category, collection_name in collection_names_categories.items():
        vectorstores['category'][category] = Chroma(
            collection_name=f"category-{collection_name}",
            embedding_function=embedding,
            persist_directory='./statics/chroma_db'
        )
    return vectorstores

def clean_content(text):
    """清理文本內容，處理特殊字符和HTML標記"""
    import re
    
    # 替換HTML實體
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    
    # 移除HTML標籤
    text = re.sub(r'<[^>]+>', '', text)
    
    # 處理反斜線
    text = text.replace('\\', '\\\\')
    
    # 統一換行符
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    return text

def format_retrieved_docs(retrieved_docs):
    """格式化檢索到的文檔"""
    retrieve_info = 'Retrieve info:\n'
    
    for doc in retrieved_docs:
        # 清理文檔內容
        clean_content_text = clean_content(doc.page_content)
        
        # 確保metadata中的值都是字符串
        title = str(doc.metadata.get('title', ''))
        doc_id = str(doc.metadata.get('id', ''))
        
        # 構建輸出字符串
        retrieve_info += f"{clean_content_text}\n - Reference simulation：{title}, id:{doc_id}\n"
    
    return retrieve_info,title,doc_id

def retrieve_simulation(vectorstores,user_info):
    """
    {
        "info": {
            "name": "",        // student's name (string)
            "grade": "",       // grade index as string ("1" to "4")
            "age": "",         // student's age (string)
            "category": [],    // category indices as strings (array of "1" to "9")
            "detail_category": [], // dynamically generated topics (array of strings)
            "rag_query": ""   // generate the query use to retreive base on info
        },
        "response": "",        // your conversational response (string)
        "complete": false      // whether all necessary info is collected (boolean)
    }
    """
    category_list = user_info['category']
    user_grade = user_info['grade']
    query = user_info['rag_query']
    print('start retrieving')
    is_retrieve = False
    retrieve_info = 'Retrieve info:\n'
    id = []
    title = []
    for category in category_list:
        category_vectorstore = vectorstores['category'][categories[int(category)]]
        if hasattr(category_vectorstore, '_collection'):
            count = category_vectorstore._collection.count()
            print(f"Collection 中的文檔數量: {count}")
        category_vectorstoreretriever = category_vectorstore.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={
                    'score_threshold': 0.2,
                    'k':3}
            )
        category_retrieved_docs = category_vectorstoreretriever.invoke(query)
        if category_retrieved_docs:
            is_retrieve = True
            category_retrieve_info,simu_title,simu_id = format_retrieved_docs(category_retrieved_docs)
            retrieve_info += f"- {category_retrieve_info}\n"
            title.append(simu_title)
            id.append(simu_id)
    grade_vectorstore = vectorstores['grade'][grade[int(user_grade)]]    
    grade_vectorstoreretriever = grade_vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                'score_threshold': 0.2,
                'k':3}
        )    
    grade_retrieved_docs = grade_vectorstoreretriever.invoke(query)
    if grade_retrieved_docs:
        is_retrieve = True
        grade_retrieve_info,simu_title,simu_id = format_retrieved_docs(grade_retrieved_docs)
        retrieve_info += f"- {grade_retrieve_info}\n"
        title.append(simu_title)
        id.append(simu_id)

    return {
        'is_retrieve': is_retrieve,
        'retrieve_info': retrieve_info,
        'title': title,
        'id': id,
    }

def summary_simulation(info, user_info=None):
    if not info:
        return None
        
    try:
        # 準備 system message，根據是否有 user_info 調整提示
        system_message = """You are a friendly physics teacher assistant. Create personalized simulation recommendations based on the student's profile and interests.

        Key points:
        1. Adapt recommendations to student's grade level and interests
        2. Explain why each simulation would be helpful for them
        3. Use encouraging, age-appropriate language
        4. Connect simulations to real-world applications they might care about
        5. And it should provide title with link(https://cosci.tw/run/?name=<id>)
        6. Encourage student to explore and ask questions
        Keep explanations concise but engaging."""
        
        # 準備 user message，加入使用者資訊
        if user_info:
            user_context = f"""Student Profile:
            - Name: {user_info['name']}
            - Grade: {user_info['grade']}
            - Age: {user_info['age']}
            - Interests: {', '.join(user_info['detail_category'])}
            - Current topic: {user_info['rag_query']}
            """
            user_message = f"Based on this student profile:\n{user_context}\n\nPlease recommend appropriate simulations from:\n{info}"
        else:
            user_message = f"Please recommend these physics simulations:\n\n{info}"
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

    
if __name__ == '__main__':
    load_vectorstores()
    info = """
    {
    "name": "a",
    "grade": "1",
    "age": "10",
    "category": [
        "1",
        "3"
    ],
    "detail_category": [
        "vehicle acceleration",
        "how speed affects braking distance",
        "the role of friction in car movement",
        "aerodynamics and car design",
        "energy efficiency in vehicles"
    ],
    "rag_query": "vehicle acceleration car speed friction aerodynamics energy efficiency"
    }
    """
    retrieve_simulation(json.loads(info))
