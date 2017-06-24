from __future__ import absolute_import

import argparse
import pytest
import os
import sys

is_python2 = sys.version_info[0] == 2

import bokeh.command.subcommands.svg as scsvg
from bokeh.command.bootstrap import main
from bokeh.util.testing import TmpDir, WorkingDir, with_directory_contents

from . import basic_svg_scatter_script, multi_svg_scatter_script

def test_create():
    import argparse
    from bokeh.command.subcommand import Subcommand

    obj = scsvg.SVG(parser=argparse.ArgumentParser())
    assert isinstance(obj, Subcommand)

def test_name():
    assert scsvg.SVG.name == "svg"

def test_help():
    assert scsvg.SVG.help == "Create standalone SVG files for one or more applications"

def test_args():
    assert scsvg.SVG.args == (

        ('files', dict(
            metavar='DIRECTORY-OR-SCRIPT',
            nargs='+',
            help="The app directories or scripts to generate SVG for",
            default=None,
        )),

        (('-o', '--output'), dict(
            metavar='FILENAME',
            action='append',
            type=str,
            help="Name of the output file or - for standard output."
        )),

        ('--args', dict(
            metavar='COMMAND-LINE-ARGS',
            nargs=argparse.REMAINDER,
            help="Any command line arguments remaining are passed on to the application handler",
        )),

    )

def test_no_script(capsys):
    with (TmpDir(prefix="bokeh-svg-no-script")) as dirname:
        with WorkingDir(dirname):
            with pytest.raises(SystemExit):
                main(["bokeh", "svg"])
        out, err = capsys.readouterr()
        if is_python2:
            too_few = "too few arguments"
        else:
            too_few = "the following arguments are required: DIRECTORY-OR-SCRIPT"
        assert err == """usage: bokeh svg [-h] [-o FILENAME] [--args ...]
                 DIRECTORY-OR-SCRIPT [DIRECTORY-OR-SCRIPT ...]
bokeh svg: error: %s
""" % (too_few)
        assert out == ""

@pytest.mark.unit
@pytest.mark.selenium
def test_basic_script(capsys):
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "svg", "scatter.py"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["scatter.svg", "scatter.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter.py' : basic_svg_scatter_script },
                            run)

@pytest.mark.unit
@pytest.mark.selenium
def test_basic_script_with_output_after(capsys):
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "svg", "scatter.py", "--output", "foo.svg"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["foo.svg", "scatter.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter.py' : basic_svg_scatter_script },
                            run)

@pytest.mark.unit
@pytest.mark.selenium
def test_basic_script_with_output_before(capsys):
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "svg", "--output", "foo.svg", "scatter.py"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["foo.svg", "scatter.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter.py' : basic_svg_scatter_script },
                            run)

@pytest.mark.unit
@pytest.mark.selenium
def test_multiple_svg_scripts(capsys):
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "svg", "scatter1.py", "scatter2.py", "scatter3.py"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["scatter1.svg", "scatter2.svg", "scatter3.svg", "scatter1.py", "scatter2.py", "scatter3.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter1.py' : basic_svg_scatter_script,
                              'scatter2.py' : basic_svg_scatter_script,
                              'scatter3.py' : basic_svg_scatter_script },
                            run)

@pytest.mark.unit
@pytest.mark.selenium
def test_basic_script_with_multiple_svg_plots(capsys):
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "svg", "scatter.py"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["scatter.svg", "scatter_1.svg", "scatter.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter.py' : multi_svg_scatter_script },
                            run)
