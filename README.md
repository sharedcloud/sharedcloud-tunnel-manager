# Sharedcloud-tunnel-manager

Tunnel manager used by `Sharedcloud` and `Sharedcloud-cli` and in charge of opening and closing tunnels between the Server and the Clients.

### Use

The following ENV vars need to be passed when creating the Docker container:

* `ACCESS_TOKEN`: Describes the token to be able to connect it.
* `FLASK_APP`: Describes the name of the app. Please use `tunnel-manager.py` here.
* `DOCKERHUB_USERNAME`: Describes the `dockerhub` username.
* `DOCKERHUB_PASSWORD`: Describes the `dockerhub` password.
                                 -e FLASK_APP=tunnel-manager.py \
                                 -e DOCKERHUB_USERNAME=${DOCKERHUB_USERNAME} \
                                 -e DOCKERHUB_PASSWORD=${DOCKERHUB_PASSWORD} \
                                 --link some-docker:docker \
Additionally, we need to link the container to a DinD (Docker in Docker) container. Please see the example
below:
```
>>> docker run -it --privileged --name some-docker \
                                -p 10000-10010:10000-10010 \  # HTTP ports defined by Sharedcloud base.py settings file
                                -p 15000-15010:15000-15010 \  # TCP ports defined by Sharedcloud base.py settings file
                                --rm \
                                -d docker:dind

>>> docker build . -t sharedcloud-tunnel-manager

>>> docker run  --rm --name sharedcloud-tunnel-manager -e ACCESS_TOKEN=<token> \
                                                       -e FLASK_APP=tunnel-manager.py \
                                                       -e DOCKERHUB_USERNAME=<username> \
                                                       -e DOCKERHUB_PASSWORD=<password> \
                                                       -p 80:80 \  # Optional: Only required if it runs in a different machine than the Sharedcloud container
                                                       --link some-docker:docker \
                                                       -d sharedcloud-tunnel-manager
```
