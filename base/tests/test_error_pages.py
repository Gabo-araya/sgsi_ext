from pytest_django.asserts import assertTemplateUsed


def test_404(client):
    response = client.get("/this-url-does-not-exist")
    assertTemplateUsed(response, "exceptions/404.pug")
