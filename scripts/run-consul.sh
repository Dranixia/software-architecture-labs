# Taken from example in task file
docker run \
    -d \
    -p 8500:8500 \
    -p 8600:8600/udp \
    --name=consul_butynets \
    consul agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0

sleep 5  # Need some time for consul to properly start up
python3 config_consul.py  # Import needed info into consul