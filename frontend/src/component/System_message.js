import React from 'react';
import {marked} from 'marked';
const System_message = (props) => {
    marked.setOptions({
        headerIds: false,
        mangle: false,
        gfm: true,
        breaks: true,
        // 禁用自動添加段落標籤
        paragraph: false
    });
    const msg = marked.parse(props.msg, { breaks: true })
        .replace(/<\/?p>/g, '')  // 移除所有的 <p> 和 </p> 標籤
        .trim();
    return(
        <div className="w-full flex justify-start"
                style={{
                display: 'flex',
                justifyContent: 'flex-start',
                margin: "4px 0",
                paddingRight: '20px', // Add space on the right for system messages
            }}
        >
            <div
                className="text-white rounded-lg"
                style={{
                wordBreak: "break-word", // 確保文字自動換行
                backgroundColor: "#bae0ff", // 背景顏色
                fontSize: "18px", // 字體大小
                padding: "12px 16px", // 內邊距
                borderRadius: "12px", // 圓角
                textAlign: "left", // 文字對齊方式
                boxSizing: "border-box", // 確保 padding 不影響寬度
                display: "inline-block", // 讓寬度依文字內容調整
                color:"black",
                justifyContent: 'flex-end',
                }}
            >
                <div dangerouslySetInnerHTML={{__html:msg}}/>
            </div>
        </div>
    );

};

export default System_message;