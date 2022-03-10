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

  - DigitalOcean databases: After it's created, instead of using the `defaultdb`, go to the _Users & Databases_ tab in the resource page, and create another one with a better name.

    **Also create a `postgres` DB**, else `dropdb`/`createdb` will fail. (This is because DO doesn't give us the password for the postgres user, which is the owner of the template0/1 databases. However a `postgres` database solves this.)

The `postgres` container in docker-compose.yml has to be kept. It has a custom entrypoint to avoid running another postgres server and creating another database in this case. With its env vars, commands like `pg_dump` automatically target the remote DB.

So you can run queries on this remote DB running this command from server:
```sh
docker-compose exec postgres psql
```

## S3

### Provided by Amazon

Create the bucket with:
- _Object Ownership: ACLs enabled_
- all _Block public access_ settings off

Add this CORS configuration (bucket --> _Permissions_ tab --> _CORS_ at the bottom), replacing with the correct Origin:
```json
[
  {
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedOrigins": ["https://django3-stg.do.magnet.cl"]
  }
]
```

And create an IAM user with this policy:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::bucket-name",
                "arn:aws:s3:::bucket-name/*"
            ]
        }
    ]
}
```
It gives access to `bucket-name` only.

Then set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_STORAGE_BUCKET_NAME` in `.env`.

### Provided by DigitalOcean

Note that **credentials give access to all the spaces in the account**
[¹](https://www.digitalocean.com/community/questions/spaces-different-keys-per-bucket)
[²](https://www.digitalocean.com/community/questions/when-if-ever-will-spaces-support-individual-access-keys)
[³](https://ideas.digitalocean.com/storage/p/access-key-per-space),
so create a dedicated account for the project, so only staging and production share credentials.

Create the space in the cloud console. Set `AWS_STORAGE_BUCKET_NAME` and `DO_SPACES_REGION` in `.env`.

In the settings of the space in the cloud console, in _CORS Configurations_ click _Add_. Add the server's url and allow `GET` and `HEAD`.

Then in _API_, in _Spaces access keys_ click _Generate New Key_. Set it in `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

TODO: Cache-Control?
