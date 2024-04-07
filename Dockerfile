From Python:3.11.2-stretch

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /Todo

# Install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Bundle app source
COPY . .

# Expose port
EXPOSE 8000

# entrypoint to run the django.sh file
ENTRYPOINT ["/Todo/todo.sh"]
