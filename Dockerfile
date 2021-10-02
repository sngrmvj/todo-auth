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

# Expose the port
EXPOSE 8000

