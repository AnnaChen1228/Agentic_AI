# Guide Agent Frontend

A React-based frontend for the interactive learning assistant system.

## Project Structure
```bash
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
  │   ├── Chat_field.js      # Main chat interface
  │   ├── Display_field.js   # Display area
  │   ├── Input_field.js     # Input field
  │   ├── Loading.js         # Loading animation
  │   ├── Send_btn.js        # Send button
  │   ├── System_message.js  # System message
  │   └── User_message.js    # User message
  ├── index.css
  ├── index.js
  ├── logo.svg
  ├── page
  │   └── Index_page.js      # Main page
  ├── reportWebVitals.js
  └── setupTests.js
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
  "id": [],                 // Array of document IDs
  "info": null,             // User information object
  "in_follow_up": false,    // Follow-up state flag
  "is_first_question": true // First question flag
}
```

#### 2. Chat Interaction
```javascript
POST /chat

// Request Headers
{
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

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
- Node.js installed
- npm package manager

## Local Development Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run start
```

The application will be available at [http://localhost:2000](http://localhost:2000)