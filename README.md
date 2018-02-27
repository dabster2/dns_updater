# dns_updater
Proxmox container AutoUpdater >> NSD server

grep to dir. /etc/pve/nodes 
diff /etc/dns_updater/control to /etc/dns_updater
if изменился то стртуем пайтоновский скрипт который по шаблону формирует конфиг, ложит в nsd далее шел рестратует сервис.
Как получилось, на сорую руку, гибрид...
