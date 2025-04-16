from RAG import info
from pathlib import Path

from RAG import info
from pathlib import Path

from RAG import retrieve

def main():
    print("Welcome to the Interactive Physics Learning System!")
    print("You can type 'exit' at any time to end the conversation.")
    
    continue_chat = True
    last_info = None
    last_complete_info = None
    in_follow_up = False
    is_first_question = True
    
    # 添加初始問候
    initial_greeting = info.chat("", False)  # 傳入空字符串觸發初始問候
    if initial_greeting and "response" in initial_greeting:
        print("\nAI:", initial_greeting["response"])
    
    while True:
        user_input = input("\nYou: ")
        
        if not in_follow_up:
            # 初始對話階段
            user_info = info.chat(user_input, continue_chat)
            print("\nAI:", user_info["response"])
            # print(user_info["info"])
            print(user_info["complete"])
            if user_info is None:
                print("Thank you for learning with us! Have a great day!")
                break
            
            if user_info.get("complete", True):
                last_complete_info = user_info['info']
                result = retrieve.retrieve_simulation(user_info['info'])
                user_info['retrieve'] = result
                # print(user_info)
                if user_info['retrieve']['is_retrieve']:
                    # print(user_info['retrieve']['retrieve_info'])
                    last_info = user_info['retrieve']['retrieve_info']
                    user_info['response'] = retrieve.summary_simulation(user_info['retrieve']['retrieve_info'],user_info['info'])
                    print("\nAI:", user_info['response'])
                    # return user_info
                    in_follow_up = True
                else:
                    # 轉入追問模式
                    in_follow_up = True
                    continue
        else:
            # 追問階段
            print('follow_up')
            if is_first_question:
                user_info = info.follow_up_chat("", last_complete_info, True)
                is_first_question = False
            else:
                user_info = info.follow_up_chat(user_input, user_info['info'], False)
            print(user_info)
            if user_info is None:
                print("An error occurred during the conversation.")
                break
                
            print("\nAI:", user_info["response"])
            last_complete_info = user_info['info']
            
            if user_info.get("complete", True):
                result = retrieve.retrieve_simulation(user_info['info'])
                user_info['retrieve'] = result
                
                if user_info['retrieve']['is_retrieve']:
                    last_info = user_info['retrieve']['retrieve_info']
                    user_info['response'] = retrieve.summary_simulation(
                        user_info['retrieve']['retrieve_info'],
                        user_info['info']
                    )
                    print("\nAI:", user_info['response'])
                    print(user_info)
                    return user_info
                print("\nAI:", user_info['response'])
            
        continue_chat = True

    return last_info


if __name__ == '__main__':
    retrieve.load_vectorstores()
    Path('./statics/rag_logs').mkdir(parents=True, exist_ok=True)
    main()