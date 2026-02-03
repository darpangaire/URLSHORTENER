# from django.db import IntegrityError, transaction
# from .models import URL


# class URLService:
#     @staticmethod
#     def create_or_get(original_url):
#         """
#         Idempotent URL creation.
#         Same long URL → same short URL.
#         """
#         existing = URL.objects.filter(original_url=original_url).first()
#         if existing:
#             return existing

#         for _ in range(5):  # retry on collision
#             try:
#                 with transaction.atomic():
#                     return URL.objects.create(original_url=original_url)
#             except IntegrityError:
#                 continue

#         raise RuntimeError("Could not generate unique short URL")
