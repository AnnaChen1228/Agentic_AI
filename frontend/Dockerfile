# 使用 Node 官方镜像
FROM node:16-alpine

# 安装必要的构建工具
RUN apk add --no-cache python3 make g++

# 设置工作目录
WORKDIR /app

# 设置 npm 配置
RUN npm config set unsafe-perm true

# 复制 package.json 并安装依赖
COPY package.json package-lock.json ./

# 安装依赖
RUN npm install && \
    npm install --save-dev @types/node && \
    npm install antd --save && \
    npm install marked --save && \
    chmod -R 777 node_modules/

# 复制源代码
COPY . .

# 确保脚本有执行权限
RUN chmod -R 777 /app/node_modules/.bin/ && \
    chmod -R 777 /app/node_modules/react-scripts/

# 设置环境变量
ENV HOST=0.0.0.0 \
    PORT=2000 \
    WDS_SOCKET_PORT=2000 \
    REACT_APP_API_URL=/api

# 构建项目
RUN npm run build

# 暴露端口
EXPOSE 2000

# 启动开发服务器
CMD ["npm", "start"]
