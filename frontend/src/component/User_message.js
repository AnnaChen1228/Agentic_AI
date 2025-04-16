import React from 'react';

const User_message = (props) => {
  
    return(
        <div className="w-full flex justify-end"
            style={{
            display: 'flex',
            justifyContent: 'flex-end',
            margin: "4px 0",
            paddingLeft: '20px', // Add space on the left for user messages
                }}
        >
            <div
                className="rounded-lg"
                style={{
                wordBreak: "break-word", // 確保文字自動換行
                backgroundColor: "#bae0ff", // 背景顏色
                fontSize: "18px", // 字體大小
                padding: "12px 16px", // 內邊距
                borderRadius: "12px", // 圓角
                textAlign: "left", // 文字對齊方式
                boxSizing: "border-box", // 確保 padding 不影響寬度
                display: "inline-block", // 讓寬度依文字內容調整
                color: "black", 
                justifyContent: 'flex-start',
                }}
            >
                {props.msg}
            </div>
        </div>
    );

};

export default User_message;