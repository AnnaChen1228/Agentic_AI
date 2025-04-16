import React from 'react';
import { Button, Flex } from 'antd';
import { SendOutlined } from '@ant-design/icons';
const Send_btn = ({ onClick }) => (
  <Flex gap="small" wrap>
    <Button 
        type="primary"
        style={{
            width: '50px', // 按钮宽度
            height: '100px', // 按钮高度
          }}
        onClick={onClick}
    >
        <SendOutlined />
    </Button>
  </Flex>
);
export default Send_btn;