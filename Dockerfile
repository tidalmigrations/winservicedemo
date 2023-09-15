FROM python:3.7-windowsservercore-1809

WORKDIR /user/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --user
COPY server.py .
COPY templates/jokes.html ./templates/jokes.html

ENTRYPOINT ["python", "server.py"]
EXPOSE 5000
