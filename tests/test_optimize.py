# pangadfs/tests/test_optimize.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

import pytest
from stevedore.driver import DriverManager
from stevedore.named import NamedExtensionManager

from pangadfs.ga import GeneticAlgorithm


def test_optimize(ctx, test_directory):
    """Tests optimize"""
    ctx.ga_settings.csvpth = test_directory / 'test_pool.csv'

	# setup plugin managers
    dmgrs = {
		k: DriverManager(namespace=f'pangadfs.{k}', name=v, invoke_on_load=True)
		for k, v in ctx.plugin_settings.driver_managers.items()
	}

    emgrs = {
		k: NamedExtensionManager(namespace=f'pangadfs.{k}', names=v, invoke_on_load=True, name_order=True)
		for k, v in ctx.plugin_settings.extension_managers.items()
	}
    
    ga = GeneticAlgorithm(ctx=ctx, driver_managers=dmgrs, extension_managers=emgrs)
    results = ga.optimize()
    assert isinstance(results, dict)