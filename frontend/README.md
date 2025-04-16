# Frontend

## Structure

```
.
├── Dockerfile
├── README.md
├── node_modules
├── package-lock.json
├── package.json
├── public
└── src
    ├── App.css
    ├── App.js 
    ├── App.test.js
    ├── component
    ├── index.css
    ├── index.js
    └── page
```

## API

### Endpoint `http://localhost:8000/api`
### Request Format
```
POST

// Headers
{
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

// Request Body
{
  "query": "Your question or search query here"
}
```
### Response Format
```
{
  "Response": "Text answer from the AI system",  // Text displayed in the chat interface
  "Link": "Document title or description",       // Title of the referenced document
  "Reference": "data:application/pdf;base64,..." // Base64-encoded document (PDF or image)
}
```

## Execute frontend
```
npm install
npm run start
```

## Notes
- The backend determines the appropriate document based on your query
- Documents are returned as base64-encoded strings with proper MIME types
- Supported document types include PDFs and various image formats