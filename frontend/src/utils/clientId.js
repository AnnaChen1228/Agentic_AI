// utils/clientId.js
const getClientId = () => {
    const timestamp = new Date().getTime();
    const random = Math.random().toString(36).substring(2, 15);
    return `user_${timestamp}_${random}`;
    
    // return clientId;
};

export { getClientId };
