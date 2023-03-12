# Sets the base image for subsequent instructions
FROM python:3.11-slim-buster


# Sets the working directory in the container  
WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev

# Copies the dependency files to the working directory
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy API file
COPY api.py /app

ENTRYPOINT [ "python" ]
CMD [ "api.py" ]