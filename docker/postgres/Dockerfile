FROM postgres:14-alpine

ARG HOST_UID=2640
ARG HOST_GID=2640
ARG WHO=magnet

# Recreate postgres user with host UID/GID.
#
# The image runs the database server as the "postgres" user (originally UID=70),
# and chowns its bind-mounted data folder.
# With this change, docker/volumes/postgres-data/ is owned by your user instead of an extraneous one.
#
# This seems to be the easiest way, because the entrypoint expects to be run as root,
# and then su-exec to postgres user.
# Maybe https://github.com/docker-library/docs/blob/master/postgres/README.md#arbitrary---user-notes is outdated?
#
# From https://github.com/docker-library/postgres/blob/master/14/alpine/Dockerfile
RUN set -eux; \
  deluser postgres; \
  # "delgroup postgres;" fails with "delgroup: unknown group postgres"
  addgroup -g $HOST_GID -S postgres; \
  adduser -u $HOST_UID -S -D -G postgres -H -h /var/lib/postgresql -s /bin/sh postgres; \
  chown -R postgres:postgres /var/lib/postgresql /var/run/postgresql

COPY magnet-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["magnet-entrypoint.sh"]
# "If CMD is defined from the base image, setting ENTRYPOINT will reset CMD to an empty value. In this scenario, CMD must be defined in the current image to have a value."
CMD ["postgres"]
