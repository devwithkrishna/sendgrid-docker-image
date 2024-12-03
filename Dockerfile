### Stage 1
# Using python:3.11-slim as base image
FROM python:3.11-slim as base

# Applications in the environment can handle UTF-8 encoded characters correctly
#Python not to generate any .pyc files
#Disabling python buffering Op
ENV LANG="C.UTF-8" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install updated packages, Install upgraded Pip versions and installing poetry
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    pip install --upgrade pip && pip install pipenv poetry


# Set Poetry to create virtual environments inside the project directory
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Set working directory
WORKDIR /app

# copy pyproject.toml
COPY pyproject.toml .

# copy sendgrid email python file
COPY sendgrid_email.py .

# poetry venv installation
RUN poetry -v install --no-ansi --no-interaction --only main

### Stage 2

# Final stage
FROM base as runtime

# Runtime non root user
RUN useradd --create-home python

# Set a work directory
WORKDIR /home/python

# copy initial work dir
COPY --from=base /app/. /home/python

# adding virtualenv to PATH variable
ENV PATH="/home/python/.venv/bin:$PATH"

# nonroot user
USER python

# executing program
CMD ["poetry", "run", "python3", "sendgrid_email.py"]