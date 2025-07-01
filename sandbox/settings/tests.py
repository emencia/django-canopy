"""
Django settings for tests
"""
from sandbox.settings.base import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Media directory dedicated to tests to avoid polluting other environment
# media directory
MEDIA_ROOT = VAR_PATH / "media-tests"  # noqa: F405

# All test are written for english language
LANGUAGE_CODE = "en"
# Ensure english language is available
if "en" not in [k for k, v in LANGUAGES]:
    LANGUAGES = LANGUAGES + (("en", "English"),)


# Don't send any email for real, just push them to the shell output
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Restrain pagination limit to ease pagination check in tests
CANOPY_ADMIN_CONTROLLER_DATA_PAGINATION = 5
