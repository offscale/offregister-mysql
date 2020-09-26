from sys import version

from fabric.context_managers import settings
from fabric.operations import run
from offutils import ensure_quoted

if version[0] == "2":
    from itertools import ifilter as filter


def create_user(
    user, mysql_password, create_with_user="root", host="localhost", execute=True
):
    sql = "CREATE USER '{user[name]}'{host} IDENTIFIED BY '{user[password]}';".format(
        user=user, host="" if host is None else "@{}".format(ensure_quoted(host))
    )
    return execute_sql(
        sql=sql,
        user=create_with_user,
        password=mysql_password,
        host=host,
        execute=execute,
    )


def create_database(
    database, mysql_password, create_with_user="root", host="localhost", execute=True
):
    users = database.get("users")
    database = database["name"]

    sql = "CREATE DATABASE {database};".format(database=ensure_quoted(database))

    if users is not None:
        sql += " {}".format(
            " ".join(
                "GRANT ALL ON {database}.* TO {user}{host};".format(
                    database=ensure_quoted(database),
                    user=ensure_quoted(user["name"]),
                    host="" if host is None else "@{}".format(ensure_quoted(host)),
                )
                for user in users
            )
        )

    return execute_sql(
        sql=sql,
        user=create_with_user,
        password=mysql_password,
        host=host,
        execute=execute,
    )


def execute_sql(sql, user, password, host, execute=True):
    if not execute:
        return sql

    with settings(prompts={'Enter password: ': password,
                           'mysql> ': ';\n{}\q'.format(sql)}):
        return run(
            "mysql {}".format(
                " ".join(
                    filter(
                        None,
                        (
                            "-h {}".format(ensure_quoted(host)) if host else None,
                            "-u {}".format(ensure_quoted(user)) if user else None,
                            "-p" if password else None,
                            #"<<< {}".format(sql),  # -e
                        ),
                    ),
                )
            ),
            quiet=True,
        )
