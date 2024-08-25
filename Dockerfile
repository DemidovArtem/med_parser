#
FROM python:3.12

#
WORKDIR /code

#
RUN apt-get update
RUN apt-get install -y libpq-dev
RUN apt-get install -y build-essential

#
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./ /code/

# Change directory to the cloned repository
WORKDIR /code/

#
CMD ["uvicorn", "parser_fastapi_app:app", "--host", "0.0.0.0", "--port", "3001"]