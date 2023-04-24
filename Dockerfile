# For more information, please refer to https://aka.ms/vscode-docker-python
FROM paddle:2.4.2

EXPOSE 9000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
WORKDIR /app
COPY . /app

ENTRYPOINT python /app/service.py
