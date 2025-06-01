import React, { useState } from 'react';
import '../App.css';
import { Button, Form, Input } from 'antd';
import { MailOutlined } from '@ant-design/icons';

function Login_field({ emailRef, setIsLogin }) {  // 修改 props 名稱
    const [email, setEmail] = useState('');  // 添加 email 狀態

    const onFinish = values => {
        console.log('Success:', values);
        if (emailRef) {
            emailRef.current = values.Email;
        }
        setEmail(values.Email);
        setIsLogin(true);
    };

    const onFinishFailed = errorInfo => {
        console.log('Failed:', errorInfo);
    };

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
            <Form
                name="basic"
                style={{
                    width: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    position: 'absolute',
                    top: '50%',
                    transform: 'translateY(-50%)'
                }}
                initialValues={{ remember: true }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
                autoComplete="off"
            >
                <Form.Item
                    name="Email"
                    rules={[{
                        type: 'email',
                        message: 'The input is not valid E-mail!',
                    }, { required: true, message: 'Please input your email!' }]}
                    style={{
                        width: '50%',
                        maxWidth: '500px',
                        margin: '0 0 20px 0'
                    }}
                >
                    <Input
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        prefix={<MailOutlined />}
                        placeholder="Email"
                        style={{ width: '100%' }}
                    />
                </Form.Item>

                <Form.Item
                    style={{
                        width: '30%',
                        maxWidth: '100px',
                        margin: 0
                    }}
                >
                    <Button
                        type="primary"
                        htmlType="submit"
                        style={{
                            width: '100%',
                            borderRadius: '8px',
                            height: '30px'
                        }}
                    >
                        Login
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
}

export default Login_field;
