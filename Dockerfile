# 使用官方的 Python 基礎映像
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製需求文件並安裝 Python 需求
COPY requirements.txt .
RUN pip install -r requirements.txt

# 複製專案文件
COPY . .

# 執行遷移並啟動伺服器
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
