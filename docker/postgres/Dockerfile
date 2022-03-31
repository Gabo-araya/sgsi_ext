FROM postgres:14-alpine

COPY magnet-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["magnet-entrypoint.sh"]
# "If CMD is defined from the base image, setting ENTRYPOINT will reset CMD to an empty value. In this scenario, CMD must be defined in the current image to have a value."
CMD ["postgres"]
