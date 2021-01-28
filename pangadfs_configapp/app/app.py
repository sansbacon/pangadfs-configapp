# pangadfs_configapp/app/app.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

import json
import logging
from pathlib import Path

from stevedore.driver import DriverManager 
from stevedore.named import NamedExtensionManager

from pangadfs.ga import GeneticAlgorithm
from pangadfs_configapp.gasettings import ctx_from_dict


DATADIR = Path(__file__).parent / 'appdata'


def run():
	"""main script"""
	# setup configuration
	data = json.loads((DATADIR / 'config.json').read_text())
	ctx = ctx_from_dict(data)
	ctx.ga_settings.csvpth = DATADIR / ctx.ga_settings.csvpth

	# setup plugin managers
	dmgrs = {
		k: DriverManager(namespace=f'pangadfs.{k}', name=v, invoke_on_load=True)
		for k, v in ctx.plugin_settings.driver_managers.items()
	}

	emgrs = {
		k: NamedExtensionManager(namespace=f'pangadfs.{k}', names=v, invoke_on_load=True, name_order=True)
		for k, v in ctx.plugin_settings.extension_managers.items()
	}

	# set up GeneticAlgorithm object
	ga = GeneticAlgorithm(ctx=ctx, driver_managers=dmgrs, extension_managers=emgrs)

	# optimize lineup
	results = ga.optimize()

	# show results
	print(results['best_lineup'])
	print(f'Lineup score: {results["best_score"]}')



if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	run()
