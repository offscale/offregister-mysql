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
## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.