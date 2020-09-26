from __future__ import print_function

from functools import partial

from fabric.context_managers import shell_env
from fabric.operations import sudo, run
from offregister_fab_utils.apt import apt_depends
from offregister_fab_utils.ubuntu.systemd import restart_systemd

from offregister_mysql.util import create_user, create_database, execute_sql


def install0(**kwargs):
    installed = lambda: run(
        'mysqld --version | while read _ _ ver _; do echo "$ver"; done', quiet=True
    )

    if sudo("dpkg -s mysql-server", quiet=True, warn_only=True).failed:
        with shell_env(DEBIAN_FRONTEND="noninteractive"):
            # TODO: Better password handling; I think this can get leaked, even with `quiet=True`?
            sudo(
                """
            debconf-set-selections <<< 'mysql-server mysql-server/root_password password {password}';
            debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password {password}';
            """.format(
                    password=kwargs["MYSQL_PASSWORD"]
                ),
                quiet=True,
            )
            apt_depends("mysql-server", "mysql-client", "libmysqlclient-dev")
            sudo("systemctl unmask mysql")
            restart_systemd("mysql")
            return "MySQL {} installed".format(installed())

    return "[Already] MySQL {} installed".format(installed())


def setup_user_db1(**kwargs):
    kw = {"mysql_password": kwargs["MYSQL_PASSWORD"], "execute": False, "host": "localhost"}

    create_user_sql, create_database_sql = partial(create_user, **kw), partial(
        create_database, **kw
    )

    sql = "{}{}".format(
        "\n".join(map(create_user_sql, kwargs["users"])) if "users" in kwargs else "",
        "\n".join(map(create_database_sql, kwargs["databases"]))
        if "databases" in kwargs
        else "",
    )

    return execute_sql(sql, user="root", password=kwargs["MYSQL_PASSWORD"], host=None)
