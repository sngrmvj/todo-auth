#Pull Base python image
FROM python:latest

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working dir
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip 
COPY . /app
RUN pip install -r requirements.txt

# Port expose
EXPOSE 8000

CMD ["python","manage.py","runserver"]

