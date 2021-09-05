#Pull Base python image
FROM python:3.9.7

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working dir
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip 
COPY . /app
RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=toDo.settings
CMD ["python","manage.py","runserver"]

