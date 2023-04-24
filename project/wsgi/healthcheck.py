def healthcheck(application, health_url):
    def healthcheck_wrapper(environ, start_response):
        if environ.get("PATH_INFO") == health_url:
            start_response("200 OK", [("Content-Type", "text/plain")])
            return []
        return application(environ, start_response)

    return healthcheck_wrapper
