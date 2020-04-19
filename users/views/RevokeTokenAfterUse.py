from django.dispatch import receiver

from graphql_jwt.refresh_token.signals import refresh_token_rotated


@receiver(refresh_token_rotated)
def revoke_refresh_token(sender, request, refresh_token, **kwargs):
    refresh_token.revoke(request)
