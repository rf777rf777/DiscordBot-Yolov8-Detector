#使用 Python 3.10.13-slim
FROM python:3.10.13-slim

#設置工作目錄
WORKDIR /app

#複製當前目錄中的所有內容到工作目錄中
COPY . .

#安裝需要的 Python package
RUN pip install --no-cache-dir wheel Discord.py requests pillow

#設置容器的入口點並運行 main.py
ENTRYPOINT ["python", "-u", "main.py"]