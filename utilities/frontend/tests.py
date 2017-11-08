import os
import random
import shutil
import string

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from sass import CompileError


class FrontendManagementTests(TestCase):
    def setUp(self):
        # Get our temp folder ready for compiled assets
        self.temp_dir = os.path.join(
            settings.BASE_DIR,
            'temp_test_' + ''.join(random.choice(string.ascii_lowercase + \
                string.digits) for i in range(8)))
        os.mkdir(self.temp_dir)

        self.source_path = os.path.join(self.temp_dir, 'src')
        os.mkdir(self.source_path)

        self.dist_path = os.path.join(self.temp_dir, 'dist')
        os.mkdir(self.dist_path)

        self.search_path = os.path.join(self.temp_dir, 'lib')
        os.mkdir(self.search_path)


    def tearDown(self):
        # Destroy the temp folder
        shutil.rmtree(self.temp_dir)


    def test_compile_primer_css(self):
        """Test compiliation of primer-css"""

        # Compiles files normally
        source_file = os.path.join(self.source_path, 'test.scss')
        with open(source_file, 'w') as f:
            f.write('@import "primer-css/index.scss"')
        call_command(
            'compilescss',
            sourcepath=self.source_path,
            distpath=self.dist_path
        )
        self.assertTrue(
            'test.css' in os.listdir(self.dist_path)
        )
        self.assertTrue(
            os.stat(os.path.join(self.dist_path, 'test.css')).st_size > 0
        )

        # Throws an error when imports fail
        with open(source_file, 'w') as f:
            f.write('@import "not-a-real-module/index.scss"')
        with self.assertRaises(CompileError):
            call_command(
                'compilescss',
                sourcepath=self.source_path,
                distpath=self.dist_path
            )