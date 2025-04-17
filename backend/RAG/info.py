from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from util.file import write_json
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

messages = [
    {
        "role": "system",  # 改用 "system" 而不是 "developer"
        "content": '''
# Science Teacher Assistant

You are a friendly science teacher. Collect essential student info through natural conversation. And finally use rag_query to retrieve simulation to student.

## Basic Info Collection Flow
1. Get student's name
2. Get education level (grade or age)
3. Get interested subjects
4. Get specific topics in chosen subjects

## Required Info
- `name`: Student's name (string) - REQUIRED
- `grade`: Education level (int, 1-4) must be 1 to 4 reference age
  1: Elementary (6-12 Grade 1 to Grade 6)
  2: Junior High (13-15 Grade 7 to Grade 9)
  3: High School (16-18 Grade 10 to Grade 12)
  4: University (19+ Undergraduate)
- `age`: Age range (string) reference grade
- `category`: Subject codes (int array) - REQUIRED
  1: Mechanics, 2: Wave, 3: Thermodynamics, 4: Optics,
  5: Electromagnetism, 6: Modern Physics, 7: Chemistry,
  8: Earth Science, 9: Other
- `detail_category`: Specific topics (string array) - REQUIRED
- `rag_query`: Search query based on info
- `response`: Your response/question
- `complete`: true when all required info available

## Complete when:
- name provided
- either grade OR age available
- at least one category selected
- at least one detail_category specified

## Guidelines
- must ask name and grade or age in first time
- Follow the Basic Info Collection Flow
- Use friendly tone
- Provide 3-5 examples when asking about subjects/topics
- Each response should focus on collecting ONE missing piece of info
- introduce in first

Return valid JSON only.
'''
    }
]


follow_up_messages = []

def get_chat_response(messages):
    try:
        completion = client.responses.create(
            model="gpt-4o-mini",
            input=messages,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "physics_learning",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "info": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "grade": {"type": "integer"},
                                    "age": {"type": "string"},
                                    "category": {
                                        "type": "array",
                                        "items": {"type": "integer"}
                                    },
                                    "detail_category": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "rag_query": {"type": "string"}
                                },
                                "required": ["name", "grade", "age", "category", "detail_category", "rag_query"],
                                "additionalProperties": False  # 添加到 info 對象
                            },
                            "response": {"type": "string"},
                            "complete": {"type": "boolean"}
                        },
                        "required": ["info", "response", "complete"],
                        "additionalProperties": False  # 添加到根對象
                    },
                    "strict": True
                }
            }
        )
        return completion.output_text
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def chat(user_input, continue_chat):
    """
    處理單次對話並返回結果
    
    Args:
        user_input: 用戶輸入的文字
        continue_chat: 是否繼續之前的對話
    
    Returns:
        Dict 包含回應信息，或者 None 如果用戶要求退出
    """
    global messages
    
    if not continue_chat:
        messages = [messages[0]]  # 保留 system prompt
    
    if user_input.lower() == 'exit':
        return None

    messages.append({"role": "user", "content": f"Please provide a JSON response for: {user_input}"})
    
    response = get_chat_response(messages)
    if response:
        response = response.replace('false','False').replace('true','True')
        print(response)
        messages.append({"role": "assistant", "content": response})
        try:
            response_dict = eval(response)
            if response_dict.get("complete", False):
                # current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                # write_json(f'./statics/rag_logs/{current_time}.jsonl', messages)
                print("\nAll necessary information has been collected.")
            
            return response_dict

        except json.JSONDecodeError:
            print("\nError: Invalid response format")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
    
    return None

def follow_up_chat(user_input, previous_info, is_first_question=False):
    """
    處理追問對話並返回結果
    
    Args:
        user_input: 用戶輸入的文字
        previous_info: 之前收集到的用戶信息 (dict)
        is_first_question: 是否是追問階段的第一個問題
    """
    global follow_up_messages
    
    if is_first_question:
        system_prompt = {
            "role": "system",
            "content": f'''
# Follow-up Guide

Continue as caring science teacher. Ask relevant follow-up questions based on previous context. Your goal is to gather enough specific information to form a detailed rag_query for simulation retrieval.

## Current Student Info (DO NOT MODIFY):
name: {previous_info.get('name')}
grade: {previous_info.get('grade')}
age: {previous_info.get('age')}

## Response Structure
- `info`: Must contain exactly these values for basic info:
  - name: "{previous_info.get('name')}"
  - grade: {previous_info.get('grade')}
  - age: "{previous_info.get('age')}"
  - category: {previous_info.get('category')}
  - detail_category: {previous_info.get('detail_category')}
  - rag_query: Detailed search query combining all gathered information

## Complete Criteria (IMPORTANT):
Set complete = True when you have gathered ALL of:
1. Student's specific learning difficulty or challenge
2. Concrete examples of what they want to learn
3. Their current understanding level
4. Enough context to form a detailed rag_query

## Guidelines
1. DO NOT change name, grade, or age values
2. Each question should focus on ONE aspect:
   - Specific difficulties they face
   - Examples of what they want to learn
   - Their current understanding
   - Preferred learning style
3. Keep responses encouraging
4. Set complete = True ONLY when you have enough specific details for a targeted simulation

Return valid JSON only.
'''
        }
        follow_up_messages = [system_prompt]
        follow_up_messages.append({
            "role": "user", 
            "content": f"Previous context: {previous_info}\nNew input: '{user_input}'\nBased on this, either ask a focused follow-up question OR if you have enough specific details, set complete=True and form a detailed rag_query."
        })
    elif user_input.lower() == 'exit':
        return None
    else:
        follow_up_messages.append({
            "role": "user", 
            "content": f"Based on the user's response: '{user_input}', evaluate if you have enough specific information to form a detailed rag_query. If yes, set complete=True and create a comprehensive rag_query. If not, ask another focused question about their specific needs or understanding."
        })
    
    response = get_chat_response(follow_up_messages)
    print(response)
    try:
        response = response.replace('false', 'False').replace('true', 'True')
        response_dict = eval(response)
        
        # 確保基本信息不變
        if 'info' in response_dict:
            response_dict['info']['name'] = previous_info.get('name')
            response_dict['info']['grade'] = previous_info.get('grade')
            response_dict['info']['age'] = previous_info.get('age')
            
            # # 保持原有的類別信息
            # if 'category' in previous_info:
            #     response_dict['info']['category'] = previous_info['category']
            # if 'detail_category' in previous_info:
            #     response_dict['info']['detail_category'] = previous_info['detail_category']
        
        follow_up_messages.append({"role": "assistant", "content": str(response_dict)})
        
        # 如果對話進行了一定輪數，評估是否有足夠信息
        if len(follow_up_messages) >= 6:  # 調整為更合理的輪數
            current_response = response_dict.get('response', '').lower()
            if ('understand' in current_response and 
                'specific' in current_response and 
                'learn' in current_response):
                response_dict['complete'] = True
        
        return response_dict
        
    except Exception as e:
        print(f"Error processing response: {str(e)}")
        print(f"Problematic response: {response}")
        return None
