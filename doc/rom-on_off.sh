#!/bin/bash

function rspios_rom() {
    initramchk=`grep initramfs /boot/config.txt`

    if [ -z "${initramchk}" ]; then
	sudo echo "initramfs initrd.gz >> /boot/config.txt"
    else
	if [ ${initramchk:0:1} == '#' ]; then
	    sudo sed -i "s/^\#initramfs/initramfs/" /boot/config.txt
	fi
    fi
}

function rspios_not_rom() {
    sudo mount -o remount,rw /mnt/root-ro
    sudo mount -o remount,rw /mnt/boot-ro

    sudo sed -i "s/^initramfs/\#initramfs/" /mnt/boot-ro/config.txt
}

if [ ! -d /mnt/root-ro ]; then
    echo "== Raspberry pi os ROM化 =="
    rspios_rom
else
    echo "== Raspberry pi os ROM化 解除 =="
    rspios_not_rom
fi

echo "   Please Reboot System..."
