FROM python:3.8

RUN mkdir /hackuniversity-2020
WORKDIR /hackuniversity-2020

# Python dependencies
RUN pip install pipenv uwsgi
COPY Pipfile .
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

# We copy the rest of the codebase into the image
COPY . .

# Expose the port uWSGI will listen on
EXPOSE 8000

ENTRYPOINT cp -r book-scroller/build/static . && uwsgi --socket :8000 --wsgi-file BookScroller/wsgi.py