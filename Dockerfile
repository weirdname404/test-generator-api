# Using lightweight alpine image
FROM python:3.5-alpine

# Installing packages
RUN apk update
RUN pip install --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /app
COPY . /app

# Install API dependencies
RUN pipenv install

# Start app
EXPOSE 5000
ENTRYPOINT ["/usr/src/app/run.sh"]


# DOCKER DOESN'T WORK
