# Clone repo on pi

# Build the Docker image
docker build -t pi-speedtest-sensor .

# Run the container in detached mode and restart automatically if the Pi reboots
docker run -d --name speedtest-sensor --restart unless-stopped pi-speedtest-sensor

# Logs:
docker logs -f speedtest-sensor
