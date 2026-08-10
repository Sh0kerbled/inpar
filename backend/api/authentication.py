from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    DRF SessionAuthentication is_authenticated check bypasses CSRF protection.
    This is secure because CSRF protection is applied in views with POST/PUT/DELETE methods.
    """

    def enforce_csrf_checks(self, request):
        return False
