FROM alpine
RUN apk add -Uq python3 ca-certificates && rm -rf /var/cache/apk/*
COPY ./ /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["python3","/app/main.py"]
