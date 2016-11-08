from django.core.management.base import BaseCommand
from django_p.pipeline import Pipe
import requests


class WordCountUrl(Pipe):

    def run(self, url):
        r = requests.get(url)
        return len(r.content.split())


class Sum(Pipe):

    def run(self, *values):
        return sum(values)


class MySearchEnginePipeline(Pipe):

    def run(self, *urls):
        results = []
        for u in urls:
            results.append((yield WordCountUrl(u)))
        yield Sum(*results)  # Barrier waits


class Command(BaseCommand):

    def handle(self, *args, **options):
        stage = MySearchEnginePipeline(
            'http://sports.sina.com.cn/',
            'https://www.techinasia.com/nix-hydra-games-startup-lina-chen',
            'https://www.techinasia.com/3-reasons-mobile-money-talent-investors-love-india')
        stage.start()
