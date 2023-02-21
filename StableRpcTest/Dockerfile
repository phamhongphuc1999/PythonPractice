FROM python:3.10
WORKDIR /app
ENV TZ Asia/Ho_Chi_Minh
COPY . /app
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "run.py" ]
