# 使用 Python 作為基礎映像
FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 複製後端代碼
COPY . .

# 暴露端口（根據你的應用）
EXPOSE 4000

# 啟動後端應用
CMD ["python", "app.py"]
