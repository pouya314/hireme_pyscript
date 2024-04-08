# Docker instructions

1. Open a terminal/command prompt in that directory.

2. Build the Docker image using the following command:

```docker build -t hireme_pyscript .```

This command builds an image named hireme_pyscript based on the Dockerfile in the current directory.

3. Once the build is complete, you can run the container using:

```docker run -p 3000:3000 hireme_pyscript```

The -p 3000:3000 option maps port 3000 from the container to port 3000 on your host machine, allowing you to access the Flask app from your browser at http://localhost:3000/.
