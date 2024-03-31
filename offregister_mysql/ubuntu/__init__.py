# -*- coding: utf-8 -*-
from __future__ import print_function

from functools import partial

from offregister_fab_utils.apt import apt_depends
from offregister_fab_utils.ubuntu.systemd import restart_systemd

from offregister_mysql.util import create_database, create_user, execute_sql


def install0(**kwargs):
    installed = lambda: c.run(
        'mysqld --version | while read _ _ ver _; do echo "$ver"; done', hide=True
    )

    if c.sudo("dpkg -s mysql-server", hide=True, warn=True).exited != 0:
        env = dict(DEBIAN_FRONTEND="noninteractive")
        # TODO: Better password handling; I think this can get leaked, even with `hide=True`?
        c.sudo(
            """
        debconf-set-selections <<< 'mysql-server mysql-server/root_password password {password}';
        debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password {password}';
        """.format(
                password=kwargs["MYSQL_PASSWORD"]
            ),
            hide=True,
            env=env,
        )
        apt_depends(c, "mysql-server", "mysql-client", "libmysqlclient-dev")
        c.sudo("systemctl unmask mysql", env=env)
        restart_systemd(c, "mysql")
        return "MySQL {} installed".format(installed())

    return "[Already] MySQL {} installed".format(installed())


def setup_user_db1(**kwargs):
    kw = {
        "mysql_password": kwargs["MYSQL_PASSWORD"],
        "execute": False,
        "host": "localhost",
    }

    create_user_sql, create_database_sql = partial(create_user, **kw), partial(
        create_database, **kw
    )

    sql = "{}{}".format(
        "\n".join(map(create_user_sql, kwargs["users"])) if "users" in kwargs else "",
        "\n".join(map(create_database_sql, kwargs["databases"]))
        if "databases" in kwargs
        else "",
    )

    execute_sql(sql, user="root", password=kwargs["MYSQL_PASSWORD"], host=None)
