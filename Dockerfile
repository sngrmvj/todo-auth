#Pull Base python image
FROM python:3.9.7

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working dir
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip 
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

# ENV variables
ENV DJANGO_SETTINGS_MODULE=toDo.settings
ENV UNWANTED_KEY='ZGphbmdvLWluc2VjdXJlLTA2JXo4aiU1anViZTJuQF93ZmE2amJlbWgtbTJnaCZxbC0mNjdkYjlecW9zeWNqIyR6'
ENV DATABASE_NAME='Y3JlZGVudGlhbHM='
ENV DATABASE_USER='cG9zdGdyZXM='
ENV DATABASE_PASSWORD='cm9vdA=='
ENV DATABASE_HOST='ZGI='
ENV DATABASE_PORT='NTQzMg=='

# Expose the port
EXPOSE 8000

