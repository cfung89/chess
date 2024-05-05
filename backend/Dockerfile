FROM python:3

WORKDIR /backend

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-m", "flask", "--app", "server", "run"]