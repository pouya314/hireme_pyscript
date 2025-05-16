# Docker instructions

1. Open a terminal/command prompt in that directory.

2. Build the Docker image using the following command:

```docker build -t hireme_pyscript .```

This command builds an image named hireme_pyscript based on the Dockerfile in the current directory.

3. Once the build is complete, you can run the container using:

```docker run --env-file ./.env -p 3000:3000 hireme_pyscript```

or combined together:

```docker build -t hireme_pyscript . && docker run --env-file ./.env -p 3000:3000 hireme_pyscript```

The -p 3000:3000 option maps port 3000 from the container to port 3000 on your host machine, allowing you to access the Flask app from your browser at http://localhost:3000/.

-------

Some helpful Kamal commands:

```kamal app containers```

```kamal rollback <VERSION>``` (use the version number from the second column)

-------
.kamal/
├── secrets.common       # Shared secrets
├── secrets.staging      # Staging-specific secrets
└── secrets.production   # Production-specific secrets
config/
├── deploy.yml           # Base config
├── deploy.staging.yml   # Staging overrides
└── deploy.production.yml # Production overrides


Load the `.env` file into the shell environment: Before running the `kamal deploy` command, make sure the variables from the `.env` file are available in your shell. You can do this by running:

```export $(grep -v '^#' .env | xargs)```

To confirm secrets are loaded correctly, run:

```kamal secrets print```

-------

# Other
Deploying FastAPI Apps Over HTTPS with Traefik:
- video: https://www.youtube.com/watch?v=7N5O62FjGDc
- code: https://github.com/tiangolo/blog-posts/tree/master/deploying-fastapi-apps-with-https-powered-by-traefik
- article: https://dev.to/tiangolo/deploying-fastapi-and-other-apps-with-https-powered-by-traefik-5dik

https://anthonynsimon.com/blog/kamal-deploy/

https://beenje.github.io/blog/posts/running-your-application-over-https-with-traefik/

PyScript resources:
- https://sites.google.com/view/pyscript/home