offregister_mysql
=================
This package follows the offregister specification for MySQL.

## Install dependencies

    pip install -r requirements.txt

## Install package

    pip install .

## Example config
With `$MYSQL_PASSWORD` environment variable:

    {
        "module": "offregister-mysql",
        "type": "fabric",
        "kwargs": {
          "MYSQL_PASSWORD": {
            "$ref": "env:MYSQL_PASSWORD"
          }
        }
    }

To setup your environment to use this config, follow [the getting started guide](https://offscale.io/docs/getting-started).

## Roadmap

  - Additional users and databases
  - Custom MySQL config
  - Clustering
