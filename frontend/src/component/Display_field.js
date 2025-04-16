import React, { useEffect, useState } from 'react';
const DisplayField = ({ data }) => {
  const [key, setKey] = useState(Date.now());
  
  // useEffect(() => {
  //   setKey(Date.now());
  // }, [data?.id]);
  // console.log(data.Reference);
//   const imageTypes = ['image/jpg', 'image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp', 'simage/vg'];
//   const isImage = data?.Reference && imageTypes.some(type => 
//     data.Reference.toLowerCase().includes(type)
//   );

//   if (isImage) {
//     return (
//       <div 
//   style={{
//     width: '100%',
//     height: '100%', // 高度佔滿父元素
//     overflowY: 'auto',
//     overflowX: 'hidden',
//   }}
// >
//   <img 
//     key={key}
//     src={data?.Reference}
//     style={{
//       maxWidth: '100%',
//       display: 'block',
//     }}
//     alt="Content"
//   />
// </div>

    // );
  // }
  
  return (
    <iframe 
      key={key}
      src={`https://cosci.tw${data?.id ? `/run/?name=${data.id}` : ''}`}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        border: 'none',
      }}
      frameBorder="0"
      marginHeight="0"
      marginWidth="0"
      scrolling="yes"
      allowFullScreen
    />
  );
};

export default DisplayField;
