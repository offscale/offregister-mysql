from fabric.context_managers import shell_env
from fabric.operations import sudo, run

from offregister_fab_utils.apt import apt_depends
from offregister_fab_utils.ubuntu.systemd import restart_systemd


def install0(**kwargs):
    installed = lambda: run('mysqld --version | while read _ _ ver _; do echo "$ver"; done', quiet=True)

    if sudo('dpkg -s mysql-server', quiet=True, warn_only=True).failed:
        with shell_env(DEBIAN_FRONTEND='noninteractive'):
            # TODO: Better password handling; I think this can get leaked, even with `quiet=True`?
            sudo('''
            debconf-set-selections <<< 'mysql-server mysql-server/root_password password {password}';
            debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password {password}';
            '''.format(password=kwargs['MYSQL_PASSWORD']), quiet=True)
            apt_depends('mysql-server', 'mysql-client', 'libmysqlclient-dev')
            sudo('systemctl unmask mysql')
            restart_systemd('mysql')
            return 'MySQL {} installed'.format(installed())

    return '[Already] MySQL {} installed'.format(installed())
