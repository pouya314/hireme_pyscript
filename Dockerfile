FROM python:3.13-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the installer
#ADD https://astral.sh/uv/install.sh /uv-installer.sh
ADD https://astral.sh/uv/0.5.29/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen --no-dev

# run
EXPOSE 3000
CMD ["uv", "run", "gunicorn", "app:app", "-b", "0.0.0.0:3000"]
