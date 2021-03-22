FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN mkdir /Downloads
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code

# Used to update monogDB at container run time.
ENTRYPOINT ["entrypoint.sh"]