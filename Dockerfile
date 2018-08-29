FROM python:3.6.5
RUN pip install pipenv

WORKDIR /app/

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system

COPY . /app

CMD python -m runner