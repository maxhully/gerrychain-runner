FROM python:3.6.5
RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy

COPY . /app

CMD pipenv run python -m runner