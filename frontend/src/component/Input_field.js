import React from 'react';
import { Input } from 'antd';

const { TextArea } = Input;

const Input_field = ({ value, onChange, onKeyPress, disabled }) => {
  return (
    <TextArea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      onKeyPress={onKeyPress}
      disabled={disabled}
      placeholder="Input text"
      style={{
        flexGrow: 1,
        padding: '8px',
        borderRadius: '4px',
        border: '1px solid #ddd',
        width: 'calc(100% - 50px)',
        marginRight: '10px',
        boxSizing: 'border-box',
        resize: 'none',
        maxHeight: '100px',
        overflowY: 'auto'
      }}
    />
  );
};

export default Input_field;
