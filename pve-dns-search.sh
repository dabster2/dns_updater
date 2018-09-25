#!/bin/bash
#pip install jinja2

CTRL_DIR=/etc/dns_updater/control
chains=pve-search.txt
filename=$chains
dt=$(date '+%d/%m/%Y %H:%M:%S');

grep -r "hostname" /etc/pve/nodes/ -A2 | awk ' {print $2}' > /etc/dns_updater/pve-search.txt

if [ "$1" = "-f" ]; then
    rm -f $CTRL_DIR/$filename
elif [ "$1" = "-s" ]; then
    $IPT -F $chains
    echo "$filename: Stopping..."
    exit
fi
if [ -f "$CTRL_DIR/$filename" ]; then
    if [ -z "`diff /etc/dns_updater/$filename $CTRL_DIR/$filename`" ]; then
        echo "$filename: Nothing to do, exiting..."
        exit
    fi
fi
cp -f /etc/dns_updater/$filename $CTRL_DIR
echo "$filename: Start DNS Update..."

python /etc/dns_updater/python/dns_updater.py --hosts /etc/pve/nodes/ --template /etc/dns_updater/template --output_config /etc/nsd/master/numus.lan
echo "nsd-control reload...."
nsd-control reload
echo "Changes in dns-name or ip addresses are noticed. Applied changes!!! $dt" | mail -s "dns_updater" sysadmins@centroit.eu
