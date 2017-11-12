import os

from django.conf import settings
from django.core.management.base import BaseCommand
import sass


class Command(BaseCommand):
    help = 'Compiles primer scss files to static css'


    def add_arguments(self, parser):
        parser.add_argument(
            '--searchpath',
            help='Additional path to include in the libsass search path',
            default=os.path.join(settings.BASE_DIR, 'utilities', 'frontend')
        )

        parser.add_argument(
            '--sourcepath',
            help=('Path to source files to be compiled (sub-directories are '
                  'not recursively processed'),
            default=os.path.join(settings.BASE_DIR, 'utilities', 'frontend', 
                'src')
        )

        parser.add_argument(
            '--distpath',
            help='Path where compiled css files should be written',
            default=os.path.join(settings.BASE_DIR, 'utilities', 'static',
                'css')
        )


    def handle(self, *args, **options):
        search_path = options['searchpath']
        source_path = options['sourcepath']
        dist_path = options['distpath']

        for source_file in [f for f in os.listdir(source_path) \
            if os.path.isfile(os.path.join(source_path, f))]:
            compiled_file = os.path.join(
                dist_path,
                source_file.split('.')[0] + '.css'
            )
            with open(compiled_file, 'w') as f:
                f.write(sass.compile(
                    include_paths=(search_path,),
                    filename=os.path.join(source_path, source_file)
                ))