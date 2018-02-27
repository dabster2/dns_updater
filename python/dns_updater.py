import subprocess
import re
import argparse
from jinja2 import Template
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class ConfigUpdater:
    def __init__(self, hosts_path, config_template, output_file, reload):
        self.hosts_path = hosts_path
        self.config_template = config_template
        self.output_file = output_file
        self.hosts = {}
        self.reload = reload

    def update(self):

        try:
            self.hosts = {}
            logger.info('update config')

            lines_hostnames = subprocess.check_output(['grep', '-r', 'hostname:', self.hosts_path]).decode(
                'utf-8').split(
                '\n')
            lines_ip = subprocess.check_output(['grep', '-r', 'ip=', self.hosts_path]).decode('utf-8').split('\n')

            # remove empty lines
            lines_hostnames = list(filter(None, lines_hostnames))
            lines_ip = list(filter(None, lines_ip))

            # we need unique config lines
            lines_hostnames = set(lines_hostnames)
            lines_ip = set(lines_ip)

            self.append_hostnames(lines_hostnames)

            self.append_ip(lines_ip)

            self.write_config()

            if self.reload:
                subprocess.check_output(['nsd-control', 'reload'])

        except Exception as e:
            logger.exception(e)

    def write_config(self):

        with open(self.config_template) as template_file, open(self.output_file, 'w+') as output_file:
            template = Template(template_file.read())
            now = datetime.utcnow()
            serial = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'\
                .format(now.year, now.month, now.day, now.hour, now.minute, now.second)
            config = template.render(serial=serial, config= self.to_text())
            output_file.write(config)

    def to_text(self):
        text = ''
        for hostname in self.hosts:
            text += hostname + '\tA\t' + self.hosts[hostname]['ip'] + '\n'

        return text

    def append_hostnames(self, configs):

        for line in configs:
            args = line.split(':')
            filename = args[0]
            hostname = args[2].strip()
            if hostname in self.hosts:
                raise Exception('duplicate hostname: {} found in {} and {}'
                                .format(hostname, filename, self.hosts[hostname]['file']))
            self.hosts[hostname] = {'file': filename}

    def append_ip(self, lines):
        for line in lines:
            args = line.split(':')
            file = args[0]

            reg_ip = "ip=\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            ip = re.search(reg_ip, line).group()

            for host in self.hosts:
                if self.hosts[host]['file'] == file:
                    self.hosts[host]['ip'] = ip[3:]


def main():
    parser = argparse.ArgumentParser(description='Updates dns config when dir with hostnames changes')

    parser.add_argument('--hosts', required=True, type=str)
    parser.add_argument('--template', required=True, type=str)
    parser.add_argument('--output_config', required=True, type=str)
    parser.add_argument('--reload', default=False, type=bool)

    args = parser.parse_args()

    config_updater = ConfigUpdater(args.hosts, args.template, args.output_config, args.reload)
    config_updater.update()


if __name__ == "__main__":
    main()
