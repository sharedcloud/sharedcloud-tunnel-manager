# Sharedcloud-tunnel-manager

Library in charge of opening and closing tunnels between the Server and the Clients.

### Installation & Use
1. `docker run -e ACCESS_TOKEN=<token> -e FLASK_APP=tunnel-manager.py -v /var/run/docker.sock:/var/run/docker.sock -p 8080:8080 sharedcloud/sharedcloud-tunnel-manager`
