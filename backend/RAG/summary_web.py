from openai import OpenAI
import os 
from dotenv import load_dotenv
load_dotenv()  

def summary_website(data):
    client = OpenAI(api_key=os.getenv('API_KEY'))
    response = client.responses.create(
        model="gpt-4.1",
        tools=[{"type": "web_search_preview"}],
        input=[
            {
                "role": "system", 
                "content": "Give the short introduction to user when system recommand this simulation to user."
            },
            {
                "role": "user",
                "content": data
            }
        ],
        text={
            "format":{
                "type": "json_schema",
                "name": "website_summary",
                "schema": {
                    "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the simulation"
                            },
                            "link": {
                                "type": "string",
                                "description": "The website URL"
                            },
                            "intro": {
                                "type": "string",
                                "description": "A brief intro of the simulation"
                            }
                        },
                        "required": ["title", "link", "intro"],
                        "additionalProperties": False
                    },
                "strict": True
            }
        }
    )
    return response.output[0].content[0].text