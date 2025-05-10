from retrieve import retrieve_simulation_hw, load_vectorstores,enhance_query
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

grades = {
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

def format_information(info):
    category_index = info['category']
    grade = grades[info['grade']]
    question = info['question']
    category = ''
    for index in category_index:
        category += categories[index]
    
    user_info = f'''
        user inofrmation:
        grade: {grade}
        category: {category}
        question: {question}
    '''
    return user_info
   
def main():
    vectorstores = load_vectorstores()
    
    user_info={
    'category': [1,3],
    'grade':2,
    'question':'free falling'
    }
    info_str = format_information(user_info)
    enhance_msg = f'''
        Please bese on user info to enhance rag query
        {info_str}
    '''

    query = eval(enhance_query(enhance_msg))['rag_query']
    print(query)
    retrieve_reslt = retrieve_simulation_hw(vectorstores,user_info,query)
    print(retrieve_reslt['retrieve_info'])

if __name__ =='__main__':
    main()
