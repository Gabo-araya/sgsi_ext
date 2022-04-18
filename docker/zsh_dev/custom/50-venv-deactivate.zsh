# Poetry's virtualenv should always be active because of VIRTUAL_ENV and PATH set in ".env".

# However, this makes "deactivate" unavailable.
# It could be manually implemented but it's not worth it.

deactivate() {
  echo 'Not implemented. Run "unset VIRTUAL_ENV" and manually edit PATH.'
  false
}
