FROM python:3.7-alpine

# Copy requirements.txt
#COPY ./requirements.txt /app/requirements.txt

# Install all the requirements
#RUN pip install -r /app/requirements.txt




RUN mkdir -p /app/out
RUN apk --update add --no-cache file imagemagick build-base jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
VOLUME /app/out
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN python -c 'import imageio; imageio.plugins.ffmpeg.download();'
ADD make_thumbnail make_thumbnail
RUN ln -s /app/make_thumbnail /bin/make_thumbnail
RUN chmod +x /app/make_thumbnail

# Copy everthing from . to /app inside the 'box'
COPY . /app
WORKDIR /app


# How to run it when we start up the box?
CMD ["python3", "factor_worker.py"]
