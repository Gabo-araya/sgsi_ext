# reCAPTCHA

To help secure the app from password bruteforce attempts, reCAPTCHA is always displayed if configured and enabled.

In case of problems with the service, the CAPTCHA can be disabled by toggling the ENABLE_LOGIN_RECAPTCHA parameter.
If you can't log in to the admin site, you can still do it over management commands:

```shell
./manage.py setparameter ENABLE_LOGIN_RECAPTCHA False
```

This feature consumes the following env variables:

- `RECAPTCHA_PUBLIC_KEY`
- `RECAPTCHA_PRIVATE_KEY`


## Using reCAPTCHA v2 or v3
By default, both admin and login views use reCAPTCHA v3. You can choose to use reCAPTCHA v2 by changing the
`RECAPTCHA_WIDGET` environment variable to one of the following values:

* django_recaptcha.widgets.ReCaptchaV3
* django_recaptcha.widgets.ReCaptchaV2Invisible
* django_recaptcha.widgets.ReCaptchaV2Checkbox

Don't forget to set the appropiate keys as environment variables.

## ReCAPTCHA v3 minimum score
The `RECAPTCHA_V3_REQUIRED_SCORE` parameter the minimum score required to pass the check.
If not set, the default is 0.65. You can set a float value from 0 (allow all) to 1 (reject all).
