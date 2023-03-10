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

# RUN mkdir /home/jovyan/.paddlenlp
# RUN mkdir /home/jovyan/.paddlenlp/models
# USER root
# RUN  chmod -R 777 /home/jovyan/.paddlenlp
# # RUN  chmod -R 777 /home/jovyan/.paddlenlp/models
# USER jovyan
# USER root
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

ENTRYPOINT python /app/service.py
