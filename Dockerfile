# Use an offical Python runtime as a parent image
FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1
ENV NAME Project
RUN mkdir /code
WORKDIR /code
COPY . /code
RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run uwsgi when the container launches
CMD ['uwsgi', '--ini', 'config/docker_uwsgi.ini']

