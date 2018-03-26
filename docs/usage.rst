=====
Usage
=====

To use telegram_bots in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'telegram_bots.apps.TelegramBotsConfig',
        ...
    )

Add telegram_bots's URL patterns:

.. code-block:: python

    from telegram_bots import urls as telegram_bots_urls


    urlpatterns = [
        ...
        url(r'^', include(telegram_bots_urls)),
        ...
    ]
