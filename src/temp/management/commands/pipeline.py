from django.core.management.base import BaseCommand
from django_p.pipeline import Pipe


class AddOne(Pipe):

    def run(self, number):
        return number + 1


class AddTwo(Pipe):

    def run(self, number):
        v = yield AddOne(number)
        yield AddOne(v)


class Command(BaseCommand):

    def handle(self, *args, **options):
        stage = AddTwo(15)
        stage.start()
