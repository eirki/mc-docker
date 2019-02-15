Dockerfile to facilite running the 113 branch of https://github.com/overviewer/Minecraft-Overviewer on a Realms map.

Download script adapted from https://github.com/air/minecraft-tools.

In order to build the docker image, rename the file `renderconfig-example.py` to ` renderconfig.py`,

then run
```
docker build --file Dockerfile . --tag mc
```
to build the image.

To run the container, create a `.env` file containing the fields EMAIL and PASSWORD, and run
```
docker run --env-file=.env --volume /tmp/render:/tmp/render  --user $(id -u):$(id -g) mc
```


