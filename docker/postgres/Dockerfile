FROM postgres:15-bullseye

ARG HOST_UID=2640
ARG HOST_GID=2640
ARG WHO=magnet
ARG POSTGRES_LOCALE=es_CL

# set locale for proper language support, keep messages in english
RUN localedef -i $POSTGRES_LOCALE -c -f UTF-8 -A /usr/share/locale/locale.alias $POSTGRES_LOCALE.UTF-8
ENV LANG="$POSTGRES_LOCALE.UTF-8"
ENV LC_MESSAGES="en_US.UTF-8"


# Recreate postgres user with host UID/GID.
#
# The image runs the database server as the "postgres" user (originally UID=999),
# and chowns its bind-mounted data folder.
# With this change, docker/volumes/postgres-data/ is owned by your user instead of an extraneous one.
#
# This seems to be the easiest way, because the entrypoint expects to be run as root,
# and then su-exec to postgres user.
# Maybe https://github.com/docker-library/docs/blob/master/postgres/README.md#arbitrary---user-notes is outdated?
#
# From https://github.com/docker-library/postgres/blob/master/14/bullseye/Dockerfile
RUN set -eux; \
  deluser postgres; \
  # "delgroup postgres;" fails with "delgroup: unknown group postgres"
  groupadd -g $HOST_GID -r postgres; \
  useradd -u $HOST_UID -r -g postgres -M -d /var/lib/postgresql -s /bin/bash postgres; \
  chown -R postgres:postgres /var/lib/postgresql /var/run/postgresql

COPY magnet-entrypoint.sh /usr/local/bin/
COPY 70-initialize-log-db.sh /docker-entrypoint-initdb.d/

ENTRYPOINT ["magnet-entrypoint.sh"]
# "If CMD is defined from the base image, setting ENTRYPOINT will reset CMD to an empty value. In this scenario, CMD must be defined in the current image to have a value."
CMD ["postgres"]
