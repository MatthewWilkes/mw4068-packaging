# -*- coding: utf-8 -*-

"""
Example Usage
=============

The following commands can be run from the root directory of the Mercurial
repo. To run ``paver``, however, you'll need to do ``easy_install Paver``.
Most of the following commands accept other arguments; see ``command --help``
for more information, or ``paver help`` for a list of all the valid commands.

    ``paver build``
        Builds the project. This essentially just runs a bunch of other tasks,
        like ``pylint`` and ``tinymce_zip``, etc.
    ``paver pylint``
        Runs PyLint on the project.
    ``paver tinymce_zip``
        Builds the TinyMCE zip file.

If you specify ``--dry-run`` before a task, then the action of that task will
not actually be carried out, although logging output will be displayed as if
it were. For example, you could run ``paver --dry-run tinymce_zip`` to see what
files would be added to the ``tinymce.zip`` file, etc.
"""

from cStringIO import StringIO
import sys
import zipfile

import paver
import paver.easy
import paver.tasks
from paver.easy import *
from paver.path import path


# Paver comes with Jason Orendorff's 'path' module; this makes path
# manipulation easy and far more readable.
PROJECT_DIR = path(__file__).dirname().abspath()


# Set some default options. Having the options at the top of the file cleans
# the whole thing up and makes the behaviour a lot more configurable.
options(
    build = Bunch(
        project_dir = PROJECT_DIR,
        app_build = PROJECT_DIR / 'build',
        app_folder = PROJECT_DIR / 'app',
        app_files = ['app.yaml', 'cron.yaml', 'index.yaml', 'queue.yaml',
                     'main.py', 'settings.py', 'urls.py', 'gae_django.py',
                     'profiler.py'],
        app_dirs =  ["soc", "feedparser", "python25src", "reflistprop",
                     "jquery", "ranklist", "shell", "json", "jlinq",
                     "htmlsanitizer", "taggable", "gviz"],
        zip_files = ['tiny_mce.zip'],
        skip_pylint = False,
        skip_closure = False,
    )
)

# The second call to options allows us to re-use some of the constants defined
# in the first call.
options(
    clean_build = options.build,
    tinymce_zip = options.build,
    
    pylint = Bunch(
        check_modules = ['soc', 'reflistprop', 'settings.py', 'urls.py',
                         'main.py'],
        quiet = False,
        quiet_args = ['--disable-msg=W0511,R0401', '--reports=no',
                      '--disable-checker=similarities'],
        pylint_args = [],
        ignore = False,
        **options.build
    )
)


# Utility functions

def tinymce_zip_files(tiny_mce_dir):
    """Yields each filename which should go into ``tiny_mce.zip``."""
    for filename in tiny_mce_dir.walkfiles():
        if '.svn' in filename.splitall():
            continue

        paver.tasks.environment.info(
            '%-4stiny_mce.zip <- %s', '', filename)
        arcname = tiny_mce_dir.relpathto(filename)
        yield filename, arcname


def write_zip_file(zip_file_handle, files):
    if paver.tasks.environment.dry_run:
        for args in files:
            pass
        return
    zip_file = zipfile.ZipFile(zip_file_handle, mode='w')
    for args in files:
        zip_file.write(*args)
    zip_file.close()


def symlink(target, link_name):
    if hasattr(target, 'symlink'):
        target.symlink(link_name)
    else:
        # If we are on a platform where symlinks are not supported (such as
        # Windows), simply copy the files across.
        target.copy(link_name)


# Tasks


@task
@cmdopts([
    ('app-folder=', 'a', 'App folder directory (default /app)'),
    ('pylint-command=', 'c', 'Specify a custom pylint executable'),
    ('quiet', 'q', 'Disables a lot of the pylint output'),
    ('ignore', 'i', 'Ignore PyLint errors')
])
def pylint(options):
    """Check the source code using PyLint."""
    from pylint import lint
    
    # Initial command.
    arguments = []
    
    if options.quiet:
        arguments.extend(options.quiet_args)
    if 'pylint_args' in options:
        arguments.extend(list(options.pylint_args))
    
    # Add the list of paths containing the modules to check using PyLint.
    arguments.extend(
        str(options.app_folder / module) for module in options.check_modules)
    
    # By placing run_pylint into its own function, it allows us to do dry runs
    # without actually running PyLint.
    def run_pylint():
        # Add app folder to path.
        sys.path.insert(0, options.app_folder.abspath())
        # Add google_appengine directory to path.
        sys.path.insert(0,
            options.project_dir.abspath() /
                'thirdparty' / 'google_appengine')
        
        # Specify PyLint RC file.
        arguments.append('--rcfile=' +
            options.project_dir.abspath() /
                'scripts' / 'pylint' / 'pylintrc')
        
        # `lint.Run.__init__` runs the PyLint command.
        try:
            lint.Run(arguments)
        # PyLint will `sys.exit()` when it has finished, so we need to catch
        # the exception and process it accordingly.
        except SystemExit, exc:
            return_code = exc.args[0]
            if return_code != 0 and (not options.pylint.ignore):
                raise paver.tasks.BuildFailure(
                    'PyLint finished with a non-zero exit code')
    
    return dry('pylint ' + ' '.join(arguments), run_pylint)


@task
@cmdopts([
    ('app-build=', 'b', 'App build directory (default /build)'),
    ('app-folder=', 'a', 'App folder directory (default /app)'),
    ('skip-pylint', 's', 'Skip PyLint checker'),
    ('ignore-pylint', 'i', 'Ignore results of PyLint (but run it anyway)'),
    ('quiet-pylint', 'q', 'Make PyLint run quietly'),
])
def build(options):
    """Build the project."""
    # If `--skip-pylint` is not provided, run PyLint.
    if not options.skip_pylint:
        # If `--ignore-pylint` is provided, act as if `paver pylint --ignore`
        # was run. Likewise for `--quiet-pylint`.
        if options.get('ignore_pylint', False):
            options.pylint.ignore = True
        if options.get('quiet_pylint', False):
            options.pylint.quiet = True
        pylint(options)
    
    # Clean old generated zip files from the app folder.
    clean_zip(options)
    
    # Clean the App build directory by removing and re-creating it.
    clean_build(options)
    
    # Build the tiny_mce.zip file.
    tinymce_zip(options)
    
    # Make the necessary symlinks between the app and build directories.
    build_symlinks(options)


@task
@cmdopts([
    ('app-build=', 'b', 'App build directory (default /build)'),
    ('app-folder=', 'a', 'App folder directory (default /app)'),
])
def build_symlinks(options):
    """Build symlinks between the app and build folders."""
    # Create the symbolic links from the app folder to the build folder.
    for filename in options.app_files + options.app_dirs + options.zip_files:
        # The `symlink()` function handles discrepancies between platforms.
        target = path(options.app_folder) / filename
        link = path(options.app_build) / filename
        dry(
            '%-4s%-20s <- %s' % ('', target, link),
            lambda: symlink(target, link.abspath()))


@task
@cmdopts([
    ('app-build=', 'b', 'App build directory (default /build)'),
])
def clean_build(options):
    """Clean the build folder."""
    # Not checking this could cause an error when trying to remove a
    # non-existent file.
    if path(options.app_build).exists():
        path(options.app_build).rmtree()
    path(options.app_build).makedirs()


@task
@cmdopts([
    ('app-folder=', 'a', 'App folder directory (default /app)'),
])
def clean_zip(options):
    """Remove all the generated zip files from the app folder."""
    for zip_file in options.zip_files:
        zip_path = path(options.app_folder) / zip_file
        if zip_path.exists():
            zip_path.remove()


@task
@cmdopts([
    ('app-folder=', 'a', 'App folder directory (default /app)'),
])
def tinymce_zip(options):
    """Create the zip file containing TinyMCE."""
    tinymce_dir = path(options.app_folder) / 'tiny_mce'
    tinymce_zip_filename = path(options.app_folder) / 'tiny_mce.zip'
    if paver.tasks.environment.dry_run:
        tinymce_zip_fp = StringIO()
    else:
        # Ensure the parent directories exist.
        tinymce_zip_filename.dirname().makedirs()
        tinymce_zip_fp = open(tinymce_zip_filename, mode='w')
    
    try:
        write_zip_file(tinymce_zip_fp, tinymce_zip_files(tinymce_dir))
    except Exception, exc:
        tinymce_zip_fp.close()
        tinymce_zip_filename.remove()
        raise paver.tasks.BuildFailure(
            'Error occurred creating tinymce.zip: %r' % (exc,))
    finally:
        if not tinymce_zip_fp.closed:
            tinymce_zip_fp.close()
