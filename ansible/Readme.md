## Deploy

The target server has to:
- be running Ubuntu 20.04
- have Docker installed
- be present in `inventory.yml`

To deploy for the first time, run:
```sh
ansible/deploy.sh dev
```
where `dev` is the name of the host in inventory.

For faster deployments after the first one, you may use:
```sh
ansible/update.sh dev
```

Containers will be recreated if their image is updated, or "when their configuration differs from the service definition". So if there have been changes to .env files, or bind-mounted configuration files, append `--recreate` to deploy/update.sh to load changes.

## Database backups

The database is automatically backed up by update.sh/deploy.sh when `git pull` changes commit.

> Warning: if `git pull` changed commit, and then the backup fails because of misconfiguration, the next attempt to update.sh will not back up because there will be no commit change.

You can manually backup with
```sh
ansible/backup-db.sh dev
```
where `dev` is the name of the host in inventory.

## Importing the DB of a server

```sh
ansible/import-db.sh stg
```
where `stg` is the name of the host in inventory.

This will create a new dump in the server, then download and restore it.

You can also append the file name of the dump, for example:
```sh
ansible/import-db.sh stg stg-2022-02-18_17-10-00.dump
```
which won't create a new dump, and just download the existing one if it's not present in your computer, and then restore it. This makes the process faster and more reproducible, as developers can work on the same dump by running the same `import-db` command.

## External database

Create the database instance before running delpoy. The database (as in `database-name`) has to be manually created.
  - AWS RDS: At the _Create database_ wizard, under _Additional configuration_ specify _Initial database name_.
  - DigitalOcean databases: After it's created, instead of using the `defaultdb`, go to the _Users & Databases_ tab in the resource page, and create another one.

The `postgres` container in docker-compose.yml has to be kept. It has a custom entrypoint to avoid running another postgres server and creating another database in this case. With its env vars, commands like `pg_dump` automatically target the remote DB.

So you can run queries on this remote DB running this command from server:
```sh
docker-compose exec postgres psql
```
