# Offline database

This directory documents the database expected by the offline server.

The supplied reference SQL dump is authoritative for the current NSOKISS schema. It was exported from MariaDB 10.11.10 and creates:

- database: `nsotien_0`
- character set: `utf8mb4`
- host used by the dump: `127.0.0.1`
- MySQL/MariaDB port: `3306`

Important tables confirmed from the dump include `users` and `players`. The server configuration on `offline-conversion` therefore uses `nsotien_0` instead of the old remote/default database name.

## Import

Place the reference dump at either:

- `database/database.sql`, or
- `database.sql` at the repository root.

Then run `database/setup.bat` from Windows. It uses the local `mysql`/`mariadb` command available in PATH and imports the dump into the local MariaDB/MySQL instance.

The dump itself is intentionally not rewritten: its schema, data, names and defaults remain the source of truth.
