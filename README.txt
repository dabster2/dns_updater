install with:
pip install git+ssh://git@gitlab.centroit.work:777/Dmytro/dns_updater.git

example of config template:

@       IN SOA ns1.numus.lan. admin.numus.lan. (
               {{serial}}     ; serial
               28800          ; refresh
               3600           ; retry
               604800         ; expire
               86400          ; minimum
               )

              IN     NS     ns1.numus.lan.

backuper	IN	A	172.16.2.1
bareos		IN	A	172.16.2.2
numus-pve1	IN	A	172.16.1.1
numus-pve2	IN	A	172.16.1.2
numus-pve3	IN	A	172.16.1.3
numus-pve4	IN	A	172.16.1.4
numus-pve5	IN	A	172.16.1.5
numus-pve6	IN	A	172.16.1.6
numus-pve7	IN	A	172.16.1.7
numus-pve8	IN	A	172.16.1.8
;----------------------------------------------------
{{config}}

