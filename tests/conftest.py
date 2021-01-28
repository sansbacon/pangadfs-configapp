# pangadfs_configapp/tests/conftest.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

import json
from pathlib import Path
import sys

import pytest

sys.path.append("../pangadfs_configapp")

from pangadfs_configapp.gasettings import ctx_from_dict


@pytest.fixture
def configfile(test_directory):
    return test_directory / 'test_config.json'


@pytest.fixture
def ctx(configfile):
    return ctx_from_dict(json.loads(configfile.read_text()))


@pytest.fixture(scope="session", autouse=True)
def root_directory(request):
    """Gets root directory"""
    return Path(request.config.rootdir)


@pytest.fixture(scope="session", autouse=True)
def test_directory(request):
    """Gets root directory of tests"""
    return Path(request.config.rootdir) / "tests"


@pytest.fixture()
def tprint(request, capsys):
    """Fixture for printing info after test, not supressed by pytest stdout/stderr capture"""
    lines = []
    yield lines.append

    with capsys.disabled():
        for line in lines:
            sys.stdout.write("\n{}".format(line))

