# coding: utf-8
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Sample'

    def handle(self, *args, **options):
        pass
