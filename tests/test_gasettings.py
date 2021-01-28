# pangadfs_configapp/tests/test_config.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License
import json
import pytest

from pangadfs_configapp.gasettings import AppSettings, ctx_from_dict


def test_ctx_from_dict(configfile, ctx):
    """Tests ctx_from_dict"""
    data = json.loads(configfile.read_text())
    ctxo = ctx_from_dict(data)
    assert isinstance(ctxo, AppSettings)
    assert ctxo == ctx