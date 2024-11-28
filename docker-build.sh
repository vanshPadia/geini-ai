#!/bin/bash

echo "Start: build and push docker image for AI on aipoc machine"

echo "Building docker image genie-ai-image:latest"
sudo docker build -t genie-ai-image:latest . || { echo "Docker build failed"; exit 1; }

echo "Saving docker image to tarball"
docker save -o genie-ai-image.tar genie-ai-image:latest || { echo "Docker save failed"; exit 1; }

echo "Copying image tar to aipoc machine"
scp genie-ai-image.tar aipoc@172.30.20.35:/home/aipoc/genie-app/container-registry/ || { echo "SCP copy failed"; exit 1; }

echo "End: build and push docker image for AI on aipoc machine"

