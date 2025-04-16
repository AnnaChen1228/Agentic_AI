# Guide Agent Backend

A FastAPI-based backend with RAG (Retrieval-Augmented Generation) capabilities for the interactive learning assistant system.

## Project Structure
```bash
.
├── Dockerfile
├── RAG
│   ├── data
│   ├── info.py            # User information handling
│   ├── preprocess.py      # Information preprocessing
│   ├── prompt.py          # Prompt templates
│   ├── retrieve.py        # Retrieval simulation
│   └── store_vectordb.py  # Vector store management
├── README.md
├── app.py                 # Main FastAPI application
├── rag_main.py           # RAG system core
├── requirements.txt
└── util
  └── file.py           # File handling utilities
```

## API Specification

### Base URL
```
http://localhost:4000
```

### API Endpoints

#### 1. Initialize Chat
```javascript
GET /chat/init

// Response Format
{
  "response": "Initial greeting message",
  "title": [],              // Array of document titles
  "id": [],                // Array of document IDs
  "info": null,            // User information object
  "in_follow_up": false,   // Follow-up state flag
  "is_first_question": true // First question flag
}
```

#### 2. Chat Interaction
```javascript
POST /chat

// Request Body
{
  "query": "User message",
  "in_follow_up": boolean,      // Follow-up state flag
  "last_complete_info": Object  // Last complete user information
}

// Response Format
{
  "response": "AI response message",
  "title": string[],        // Array of relevant document titles
  "id": string[],          // Array of document IDs
  "info": Object,          // User information object
  "in_follow_up": boolean, // Follow-up state flag
  "is_first_question": boolean,
  "complete": boolean      // Current interaction completion status
}
```

## Prerequisites
- Python 3.11+
- FastAPI
- OpenAI API key
- Chroma DB

## Local Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the development server:
```bash
python app.py
```

The API will be available at [http://localhost:4000](http://localhost:4000)

## RAG System Setup

1. Preprocess information:
```bash
python preprocess.py
```

2. Build vector store (if needed):
```bash
python store_vectordb.py
```

## Key Features
- FastAPI-based REST API
- RAG (Retrieval-Augmented Generation) system
- Vector store management with Chroma DB
- CORS middleware enabled
- Automatic vector store initialization
- Error handling and status monitoring