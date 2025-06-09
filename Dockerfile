FROM python:3.12-slim-bookworm

# file structure:
# server-side
#     |- modelling
#     |- static
#     |- .env
#     |- index.py
#     |- server.py
#     |- requirements.txt
# Dockerfile
# readme.md

# copy local machines path to requirements.txt
# to containers directory
COPY ./server-side/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p ./server-side

# copy local server-side dir's contents into the newly made
# server-side dir in the docker container 
COPY server-side ./server-side

# switch to server-side directory
WORKDIR /server-side

# EXPOSE 5000

# CMD ["python", "index.py"]

# Expose default port
EXPOSE 7860

# Run with Gunicorn with 4 workers and bind host to port 7860
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:7860", "index:app"]

