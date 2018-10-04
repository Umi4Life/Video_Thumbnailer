# Build upon this image "alpine" is a lightweight distro
FROM python:3.7-alpine

# Copy in requirements.txt first (for caching purposes)
COPY requirements.txt /app/requirements.txt

# Install all the requirements
RUN pip install -r /app/requirements.txt

# Copy everthing from . to /app inside the 'box'
COPY . /app
WORKDIR /app


# How to run it when we start up the box?
#CMD ["gunicorn", "-b 0.0.0.0:5000", "-w 2", "main:app"]


ENV FLASK_APP=main
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]
