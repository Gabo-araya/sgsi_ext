#!/bin/sh

# Comments settings in nginx.conf that can't have duplicates.
# An alternative is to copy nginx.conf from image to repo, but diff is harder to see
# and image upgrades require updating the config too.

sed -i 's/ keepalive_timeout / #keepalive_timeout /' /etc/nginx/nginx.conf
