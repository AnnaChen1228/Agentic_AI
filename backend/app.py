from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from RAG.info import chat, follow_up_chat
from RAG import retrieve
import json

app = FastAPI()
vectorstores = None
is_initialized = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FIRST_RUN = True  # 全局參數控制是否為首次運行

@app.on_event("startup")
async def startup_event():
    global vectorstores, is_initialized, FIRST_RUN
    if not is_initialized:
        print("Checking vector stores...")
        try:
            if FIRST_RUN:
                print("Initializing vector stores for the first time...")
                FIRST_RUN = False
            
            vectorstores = retrieve.load_vectorstores()
            is_initialized = True
            print("Vector stores loaded successfully")
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            raise e

@app.middleware("http")
async def check_vectorstores(request: Request, call_next):
    if not is_initialized and request.url.path not in ["/", "/health"]:
        raise HTTPException(
            status_code=503,
            detail="Vector stores not initialized"
        )
    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/chat/init")
async def init_chat():
    try:
        print('init')
        initial_greeting = chat("Hi this is first time to talk introduce youself and ask me some question to fill the info", False)
        
        if initial_greeting is None:
            return {
                "response": "Hi I'm guide agent. How can I help you?",
                "title": [],
                "id": [],
                "info": None,
                "in_follow_up": False,
                "is_first_question": True
            }
        
        return {
            "response": initial_greeting.get("response", "Hi I'm guide agent. How can I help you?"),
            "title": [],
            "id": [],
            "info": initial_greeting.get("info", None),
            "in_follow_up": False,
            "is_first_question": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_endpoint(request: Request):
    global vectorstores
    print('chat')
    try:
        body = await request.body()
        json_body = json.loads(body)
        
        if 'query' not in json_body:
            raise HTTPException(status_code=400, detail="Query not provided")
            
        query = json_body['query']
        in_follow_up = json_body.get('in_follow_up', False)
        last_complete_info = json_body.get('last_complete_info', None)
        
        if not in_follow_up:
            user_info = chat(query, True)
            print("Chat response:", user_info)
            
            if user_info is None:
                return {
                    "response": "Chat ended",
                    "title": [],
                    "id": [],
                    "info": None,
                    "in_follow_up": False,
                    "is_first_question": False
                }
            
            if user_info.get("complete", True):
                result = retrieve.retrieve_simulation(vectorstores, user_info['info'])
                user_info['retrieve'] = result
                print(user_info)
                if result.get('is_retrieve', True):
                    response = retrieve.summary_simulation(
                        result['retrieve_info'],
                        user_info['info']
                    )
                    print(response)
                    return {
                        "response": response,
                        "title": result.get('title', []),
                        "id": result.get('id', []),
                        "info": user_info['info'],
                        "in_follow_up": True,
                        "is_first_question": False,
                        "complete": True
                    }
                else:
                    print('follow_up')
                    print(user_info)
                    user_info = follow_up_chat(query, user_info['info'], True)
                    return {
                        "response": user_info['response'],
                        "title": [],
                        "id": [],
                        "info": user_info['info'],
                        "in_follow_up": True,
                        "is_first_question": False,
                        "complete": False
                    }
            return {
                "response": user_info['response'],
                "title": [],
                "id": [],
                "info": user_info['info'],
                "in_follow_up": False,
                "is_first_question": False,
                "complete": False
            }
            
        else:
            
            user_info = follow_up_chat(query, last_complete_info, False)
            
            print("Follow-up response:", user_info)
            
            if user_info is None:
                return {
                    "response": "Chat error occurred",
                    "title": [],
                    "id": [],
                    "info": None,
                    "in_follow_up": False,
                    "is_first_question": False
                }
            
            if user_info.get("complete", True):
                result = retrieve.retrieve_simulation(vectorstores, user_info['info'])
                
                if result.get('is_retrieve', True):
                    print(response)
                    response = retrieve.summary_simulation(
                        result['retrieve_info'],
                        user_info['info']
                    )
                    return {
                        "response": response,
                        "title": result.get('title', []),
                        "id": result.get('id', []),
                        "info": user_info['info'],
                        "in_follow_up": True,
                        "is_first_question": False,
                        "complete": True
                    }
            
            return {
                "response": user_info['response'],
                "title": [],
                "id": [],
                "info": user_info['info'],
                "in_follow_up": True,
                "is_first_question": False,
                "complete": False
            }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        print("Unexpected error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=4000, reload=True)
