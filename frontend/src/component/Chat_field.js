import React, { useEffect, useRef, useState, useCallback } from 'react';
import '../App.css';
import Input_field from './Input_field.js';
import Send_btn from './Send_btn.js';
import System_message from './System_message.js';
import User_message from './User_message.js';
import Loading from './Loading.js';

function Chat_field({ onDataUpdate }) {
  const messagesEndRef = useRef(null);
  const initRef = useRef(false);
  const [userInput, setUserInput] = useState('');
  const [chatHistory, setChatHistory] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isInitialized, setIsInitialized] = useState(false);

  const [chatState, setChatState] = useState({
    in_follow_up: false,
    is_first_question: true,
    last_complete_info: null
  });

  // 使用 useCallback 記憶化初始化函數
  const initializeChat = useCallback(async () => {
    if (initRef.current) return; // 防止重複初始化
    initRef.current = true;

    try {
      const response = await fetch('http://localhost:4000/chat/init', {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      setChatState(prevState => ({
        ...prevState,
        in_follow_up: false,
        is_first_question: true,
        last_complete_info: data.info || null
      }));

      setChatHistory([
        { type: 'system', content: data.response }
      ]);
      setIsInitialized(true);
    } catch (error) {
      console.error('Initialization error:', error);
      setChatHistory([
        { type: 'system', content: "Hi I'm guide agent. How can I help you?" }
      ]);
      setIsInitialized(true);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleButtonClick = useCallback(async () => {
    if (!userInput.trim() || !isInitialized) return;
    
    const currentMessage = userInput.trim();
    setUserInput('');
    setChatHistory(prev => [...prev, { type: 'user', content: currentMessage }]);
    
    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:4000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          query: currentMessage,
          in_follow_up: chatState.in_follow_up,
          is_first_question: chatState.is_first_question,
          last_complete_info: chatState.last_complete_info
        })
      });
    
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    
      const data = await response.json();
      
      setChatState(prevState => ({
        ...prevState,
        in_follow_up: data.in_follow_up ?? false,
        is_first_question: false,
        last_complete_info: data.info
      }));
      
      if (data?.title?.length && data?.id?.length) {
        onDataUpdate({
          title: Array.isArray(data.title) ? data.title[0] : data.title,
          id: Array.isArray(data.id) ? data.id[0] : data.id
        });
      }
      
      setChatHistory(prev => [...prev, { 
        type: 'system', 
        content: data.response
      }]);
          
    } catch (error) {
      console.error('Error:', error);
      setChatHistory(prev => [...prev, { 
        type: 'error', 
        content: '發生錯誤，請稍後再試'
      }]);
      
      setChatState({
        in_follow_up: false,
        is_first_question: true,
        last_complete_info: null
      });
    } finally {
      setIsLoading(false);
    }
  }, [userInput, isInitialized, chatState, onDataUpdate]);

  const handleKeyPress = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey && !isLoading && isInitialized) {
      e.preventDefault();
      handleButtonClick();
    }
  }, [handleButtonClick, isLoading, isInitialized]);

  // 處理滾動效果
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatHistory]);

  // 初始化效果
  useEffect(() => {
    const abortController = new AbortController();
    
    if (!initRef.current) {
      initializeChat();
    }

    return () => {
      abortController.abort();
    };
  }, [initializeChat]);

  if (!chatHistory) {
    return (
      <div style={{
        border: '2px solid #69c0ff',
        borderRadius: '12px',
        padding: '16px',
        width: '100%',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        position: 'relative',
        margin: 0,
        boxSizing: 'border-box'
      }}>
        <Loading size={''} />
      </div>
    );
  }

  return (
    <div style={{
      border: '2px solid #69c0ff',
      borderRadius: '12px',
      padding: '16px',
      width: '100%',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'flex-start',
      overflowY: 'auto',
      position: 'relative',
      margin: 0,
      boxSizing: 'border-box'
    }}>
      <p style={{
        margin: '0 0 20px 0',
        textAlign: 'center',
        color: 'black',
        fontSize: '20px',
        fontWeight: 'bold'
      }}>Guide Agent</p>

      <div style={{ 
        flexGrow: 1, 
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        paddingRight: '8px'
      }}>
        {chatHistory.map((message, index) => (
          <div key={index}>
            {message.type === 'system' && (
              <System_message msg={message.content} />
            )}
            {message.type === 'user' && (
              <User_message msg={message.content} />
            )}
            {message.type === 'error' && (
              <div style={{
                padding: '8px',
                backgroundColor: '#ffebee',
                color: '#d32f2f',
                borderRadius: '8px',
                margin: '4px 0'
              }}>
                {message.content}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div style={{
            padding: '8px',
            textAlign: 'left',
          }}>
            <div className="text-white rounded-lg" style={{
              wordBreak: "break-word",
              backgroundColor: "#bae0ff",
              fontSize: "16px",
              padding: "12px 16px",
              borderRadius: "12px",
              textAlign: "left",
              boxSizing: "border-box",
              display: "inline-block",
              color: "black",
              justifyContent: 'flex-end',
            }}>
              <Loading size={''} />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div style={{
        marginTop: '16px',
        display: 'flex',
        alignItems: 'stretch',
        gap: '8px'
      }}>
        <Input_field 
          value={userInput}
          onChange={setUserInput}
          onKeyPress={handleKeyPress}
          disabled={isLoading || !isInitialized}
        />
        <Send_btn 
          onClick={handleButtonClick}
          disabled={isLoading || !isInitialized}
        />
      </div>
    </div>
  );
}

export default Chat_field;
