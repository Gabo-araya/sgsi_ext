def healthcheck(application, health_url):
    async def healthcheck_wrapper(scope, receive, send):
        if scope.get("path") != health_url:
            await application(scope, receive, send)
            return
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"text/plain")],
            }
        )
        await send({"type": "http.response.body"})

    return healthcheck_wrapper
