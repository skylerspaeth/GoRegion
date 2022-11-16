# Dev Environment Docker Image

This folder contains the Dockerfile used to generate the GoRegion development and testing image.
The purpose of this image is to enable people to test functionality of and iterate on GoRegion.

## Building
To turn the Dockerfile into an image you can run and test with, run the following command:
```bash
docker build -t goregion-dev-env .
```

## Running
Due to Docker security features, using `iptables` within a container requires you to pass the `--cap-add=NET_ADMIN` argument to your `docker run` command like so:
```bash
docker run --cap-add=NET_ADMIN -it goregion-dev-env
```
