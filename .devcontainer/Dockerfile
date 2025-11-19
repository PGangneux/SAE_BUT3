FROM python:3.14-slim

ENV NVM_VERSION=24

RUN apt update && apt install -y build-essential git curl wget unzip zip

RUN mkdir /app
WORKDIR /app
COPY ../backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
RUN bash -c "source $HOME/.bashrc && nvm install $NVM_VERSION && nvm use $NVM_VERSION && nvm alias default $NVM_VERSION"
