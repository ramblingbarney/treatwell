FROM python:3.13-slim-bookworm

ENV CATEGORIES="action-adventure,animation,classic,comedy,drama,horror,family,mystery,scifi-fantasy,western"
ENV API_URL="https://api.sampleapis.com/movies"
ENV BUCKET="movies-raw"

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
