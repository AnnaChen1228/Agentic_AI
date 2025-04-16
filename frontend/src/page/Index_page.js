import React, { useState, useCallback } from 'react';
import { Flex, Layout, theme } from 'antd';
import DisplayField from '../component/Display_field';
import ChatField from '../component/Chat_field';
import Loading from '../component/Loading'
const { Header, Content, Footer, Sider } = Layout;

const IndexPage = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  
  const [displayData, setDisplayData] = useState({
    title: 'https://cosci.tw/',
    id: '',
  });

  // 使用 useCallback 來記憶化函數
  const handleDataFromChat = useCallback((data) => {
    setDisplayData({
      title: data.title,
      id: data.id
    });
  }, []); // 空依賴數組，因為這個函數不依賴任何外部變量

  return (
    <Layout 
      hasSider 
      style={{ 
        height: '100vh',
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'row'
      }}
    >
      <Layout style={{ 
        width: '65%',
        height: '100%',
        overflow: 'hidden'
      }}>
        <Header style={{
          padding: '0 16px',
          background: colorBgContainer,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontSize: '16px',
          whiteSpace: 'nowrap',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          height: '64px',
          lineHeight: '64px'
        }}>
          {displayData.title || 'Searching....'}
        </Header>
        <Content style={{
          height: 'calc(100vh - 64px)',
          overflow: 'hidden',
          position: 'relative',
          display: 'flex',
          flexDirection: 'column'
        }}>
          {displayData.title === '' ? (
            <Flex 
              align="center" 
              justify="center"
              style={{ 
                height: '100%',
                width: '100%'
              }}
            >
              <Loading size='large' />
            </Flex>
          ) : (
            <div style={{
              flex: 1,
              width: '100%',
              height: '100%',
              position: 'relative',
              overflow: 'hidden !important'
            }}>
              <DisplayField 
                data={{ id: displayData.id }}
              />
            </div>
          )}
        </Content>
      </Layout>
      <Layout style={{ 
        width: '35%',
        height: '100%',
        overflow: 'hidden'
      }}>
        <ChatField onDataUpdate={handleDataFromChat} />
      </Layout>
    </Layout>
  );
};

export default IndexPage;
