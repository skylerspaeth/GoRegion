# Dev Environment Docker Image

This folder contains the Dockerfile used to generate the GoRegion development and testing image.
The purpose of this image is to enable people to test functionality of and iterate on GoRegion.

## Pulling
The dev environment image is available on Docker Hub, so you can easily clone it using:
```bash
docker pull skyspa/goregion-dev-env:latest
```

## Building
To build the Dockerfile into an image manually, run the following command:
```bash
docker build -t goregion-dev-env .
```

## Running
Due to Docker security features, using `iptables` within a container requires you to pass the `--cap-add=NET_ADMIN` argument to your `docker run` command like so:
```bash
docker run --cap-add=NET_ADMIN -it goregion-dev-env
```
