FROM python:3-alpine3.7

# Install any needed packages specified in requirements.txt
RUN pip install Flask==0.11.1
RUN pip install viberbot==1.0.11
RUN pip install bs4

#RUN apt-get update && apt-get -q install -y --force-yes \
#    curl \
#    python-pip
RUN mkdir /app

# Copy the current directory contents into the container at /app
ADD ./viberChuckBot.py /app/app.py

# Set the working directory to /app
WORKDIR /app

# Make port 28888 available to the world outside this container
EXPOSE $PORT
CMD ["python", "app.py"]
