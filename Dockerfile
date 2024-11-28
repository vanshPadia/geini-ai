FROM python:3.12

WORKDIR /genie-ai-app

COPY ./requirements.txt /genie-ai-app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /genie-ai-app/requirements.txt

COPY ./app /genie-ai-app/app

CMD ["fastapi", "run", "--port", "8000"]
