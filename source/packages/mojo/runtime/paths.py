"""
.. module:: paths
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the :class:`TaskBase` object which is used as the base.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

# pylint: disable=global-statement

from cgitb import lookup
from typing import List, Optional

import os
import tempfile

from mojo.collections.contextpaths import ContextPaths
from mojo.collections.wellknown import ContextSingleton

DIR_CACHE_DIRECTORY = None
DIR_DIAGNOSTICS_DIRECTORY = None
DIR_RESULTS_DIRECTORY = None
DIR_TESTRESULTS_DIRECTORY = None
DIR_TESTCASE_BYPRODUCTS_DIRECTORY = None

TRANSLATE_TABLE_NORMALIZE_FOR_PATH = str.maketrans(",.:;", "    ")

DEFAULT_PATH_EXPANSIONS = [
    os.path.expanduser,
    os.path.expandvars,
    os.path.abspath
]

def expand_path(path_in, expansions=DEFAULT_PATH_EXPANSIONS):

    path_out = path_in
    for expansion_func in expansions:
        path_out = expansion_func(path_out)

    return path_out

def collect_python_modules(search_dir: str, max_depth=None) -> List[str]:
    """
        Walks a directory tree of python modules and collects the names
        of all of the python module files or .py files.  This method allows
        for python namespaces by not forcing the root folder to contain a
        __init__.py file.

        :params searchdir: The root directory to search when collecting python modules.
    """
    pyfiles = []

    search_dir = os.path.abspath(search_dir)
    search_dir_len = len(search_dir)

    for root, _, files in os.walk(search_dir, topdown=True):

        if max_depth is not None:
            dir_leaf = root[search_dir_len:].strip(os.path.sep)
            depth = 0
            if dir_leaf != '':
                dir_leaf_parts = dir_leaf.split(os.path.sep)
                depth = len(dir_leaf_parts)
                if depth > max_depth:
                    break

        for fname in files:
            fbase, fext = os.path.splitext(fname)
            if fext == '.py' and fbase != "__init__":
                ffull = os.path.join(root, fname)
                pyfiles.append(ffull)

    return pyfiles

def ensure_directory_is_package(package_dir: str, package_title: Optional[str] = None):
    """
        Ensures that a directory is represented to python as a package by checking to see if the
        directory has an __init__.py file and if not it adds one.

        :param package_dir: The direcotry to represent as a package.
        :param package_title: Optional title to be written into the documentation string in the package file.
    """
    package_dir_init = os.path.join(package_dir, "__init__.py")
    if not os.path.exists(package_dir_init):
        with open(package_dir_init, 'w') as initf:
            initf.write('"""\n')
            if package_title is not None:
                initf.write('   %s\n' % package_title)
            initf.write('"""\n')
    return

def get_directory_for_cached_files(create=True) -> str:
    """
        Returns the path to the {home}/cache directory.
    """

    global DIR_CACHE_DIRECTORY

    if DIR_CACHE_DIRECTORY is None:
        ctx = ContextSingleton()

        runtime_home_dir = get_expanded_path(ctx.lookup(ContextPaths.RUNTIME_HOME_DIRECTORY))
        DIR_CACHE_DIRECTORY = os.path.join(runtime_home_dir, "cache")
        if create and not os.path.exists(DIR_CACHE_DIRECTORY):
            os.makedirs(DIR_CACHE_DIRECTORY)

    return DIR_CACHE_DIRECTORY

def get_directory_for_code_container(container: str) -> str:
    """
        Returns the directory for a code container (module or package)

        :param container: The code container you want to get a directory for.

        :returns: The string that represents the parent directory of the code
                  container specified.
    """
    if hasattr(container, '__path__'):
        container_dir = str(container.__path__[0]).rstrip(os.sep)
    elif hasattr(container, '__file__'):
        container_dir = os.path.dirname(container.__file__).rstrip(os.sep)
    else:
        raise RuntimeError("Unable to get parent dir for module") from None

    return container_dir

def get_expanded_path(path: str) -> str:
    """
        Returns a path expanded using expanduser, expandvars and abspath for
        the provided path.

        :param path: A path which you want to expand to a full path, expanding the
                     user, variables and relative path syntax.

        :returns: The expanded path
    """
    exp_path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
    return exp_path

def get_files_for_credentials() -> str:
    """
        Returns the paths to the credentials files.
    """

    ctx = ContextSingleton()
    files = get_expanded_path(ctx.lookup(ContextPaths.CONFIG_CREDENTIAL_URIS))

    return files

def get_files_for_landscape() -> str:
    """
        Returns the paths to the landscape files.
    """

    ctx = ContextSingleton()
    files = get_expanded_path(ctx.lookup(ContextPaths.CONFIG_LANDSCAPE_URIS))

    return files

def get_files_for_runtime() -> str:
    """
        Returns the paths to the landscape files.
    """

    ctx = ContextSingleton()
    files = get_expanded_path(ctx.lookup(ContextPaths.CONFIG_RUNTIME_URIS))

    return files

def get_files_for_topology() -> str:
    """
        Returns the paths to the topology files.
    """

    ctx = ContextSingleton()
    files = get_expanded_path(ctx.lookup(ContextPaths.CONFIG_TOPOLOGY_URIS))

    return files

def get_path_for_artifacts(label: str) -> str:
    """
        Returns a path in the form (testresultdir)/artifacts/(label)

        :param label: A label to associate with the collection of artifacts. The label is used for
                      the name of the artifact container folder.

        :returns: A path that is descendant from (testresultdir)/artifacts
    """
    trdir = get_path_for_output()
    afdir = os.path.join(trdir, "artifacts", label)

    if not os.path.exists(afdir):
        os.makedirs(afdir)

    return afdir

def get_path_for_output(create=True) -> str:
    """
        Returns the timestamped path where test results and artifacts are deposited to
    """
    global DIR_RESULTS_DIRECTORY

    if DIR_RESULTS_DIRECTORY is None:
        ctx = ContextSingleton()

        DIR_RESULTS_DIRECTORY = get_expanded_path(ctx.lookup(ContextPaths.OUTPUT_DIRECTORY))
        if create and not os.path.exists(DIR_RESULTS_DIRECTORY):
            os.makedirs(DIR_RESULTS_DIRECTORY)

    return DIR_RESULTS_DIRECTORY

def get_path_for_diagnostics(label: str) -> str:
    """
        Returns a path in the form (testresultdir)/diagnostics/(label)

        :param label: A label to associate with the collection of diagnostic captures.
                      The label is used for the name of the diagnostic container folder.

        :returns: A path that is descendant from (testresultdir)/diagnostics

        .. notes: Paths that are relative to the output directory should always call
                  get_path_for_output instead of calling for the directory of any
                  one job type.
    """


    trdir = get_path_for_output()
    diagnostics_dir = os.path.join(trdir, "diagnostics", label)

    if not os.path.exists(diagnostics_dir):
        os.makedirs(diagnostics_dir)

    return diagnostics_dir

def get_path_for_testresults() -> str:
    """
        Returns the path to the testresults directory.

        :returns: The path to the testresults directory

        ..note : This path is generally only used by the commandline because
        it can intentionally provide a different result than get_path_for_output
        if the current job is not a TESTRUN job.  If your running in a TESTRUN job,
        utilize get_path_for_output instead of this API.
    """

    global DIR_TESTRESULTS_DIRECTORY

    if DIR_TESTRESULTS_DIRECTORY is None:
        ctx = ContextSingleton()

        tr_dir = get_expanded_path(ctx.lookup(ContextPaths.RESULT_PATH_FOR_TESTS))

        DIR_TESTRESULTS_DIRECTORY = tr_dir

        if not os.path.exists(DIR_TESTRESULTS_DIRECTORY):
            os.makedirs(DIR_TESTRESULTS_DIRECTORY)

    return DIR_TESTRESULTS_DIRECTORY

def get_path_for_testcase_by_products(test_id: str) -> str:
    """
        Returns a path to the tc-by-products
    """

    global DIR_TESTCASE_BYPRODUCTS_DIRECTORY

    if DIR_TESTCASE_BYPRODUCTS_DIRECTORY is None:

        trdir = get_path_for_testresults()
        DIR_TESTCASE_BYPRODUCTS_DIRECTORY = os.path.join(trdir, "tc-by-products", test_id)

        if not os.path.exists(DIR_TESTCASE_BYPRODUCTS_DIRECTORY):
            os.makedirs(DIR_TESTCASE_BYPRODUCTS_DIRECTORY)

    return DIR_TESTCASE_BYPRODUCTS_DIRECTORY

def get_summary_html_template_source() -> str:
    """
        Looks up a source path for the summary html template.

        :returns: The path to the html summary template
    """
    ctx = ContextSingleton()

    template = get_expanded_path(ctx.lookup(ContextPaths.FILE_RESULTS_TEMPLATE))

    if template is None:
        errmsg = "Error attempting to lookup the summary html template source."
        raise RuntimeError(errmsg)

    return template

def get_summary_static_resource_dest_dir(create=True) -> str:
    """
        Returns the path where the static resources for test summaries should be published.
    """
    ctx = ContextSingleton()
    res_dir = get_expanded_path(ctx.lookup(ContextPaths.DIR_RESULTS_RESOURCE_DEST))

    if create and not os.path.exists(res_dir):
        os.makedirs(res_dir)

    return res_dir

def get_summary_static_resource_src_dir() -> str:
    """
        Returns the path that is the source path for the test summary static resources.
    """
    ctx = ContextSingleton()
    res_dir = get_expanded_path(ctx.lookup(ContextPaths.DIR_RESULTS_RESOURCE_SRC))

    return res_dir

def get_temporary_directory() -> str:
    """
        Returns the path of a temporary directory in the output directory.
    """
    temp_dir = os.path.join(get_path_for_output(), "temp")

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    return temp_dir

def get_temporary_file(suffix: str = '', prefix: str = '') -> str:
    """
        Returns the path of a temporary file in the output directory.
    """
    tempdir = get_temporary_directory()

    tmpfile = tempfile.mktemp(suffix=suffix, prefix=prefix, dir=tempdir)

    return tmpfile

def normalize_name_for_path(name: str) -> str:
    """
        Normalizes a path string by replacing ",.:;" with space and then removing
        white space.

        :param name: A name as a str which is to be normalized to allow it to be used in a path.

        :returns: The normalized string which can be used in a path.
    """
    norm_name = name.translate(TRANSLATE_TABLE_NORMALIZE_FOR_PATH).replace(" ", "")
    return norm_name

def utilizing_shared_output_path() -> bool:
    """
        Returns a boolean value indicating the runtime is configured to use a shared output
        path across compute resources.
    """

    ctx = ContextSingleton()

    op_is_shared = ctx.lookup(ContextPaths.OUTPUT_DIRECTORY_IS_SHARED, False)

    return op_is_shared
