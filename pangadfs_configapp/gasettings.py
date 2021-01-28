# pangadfs_configapp/gasettings.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

from dataclasses import dataclass, field
import logging
from typing import Any, Dict, Iterable

import dacite


logging.getLogger(__name__).addHandler(logging.NullHandler())


@dataclass
class GASettings:
    csvpth: str = 'pool.csv'
    crossover_method: str = 'uniform'
    elite_divisor: int = 5
    elite_method: str = 'fittest'
    mutation_rate: float = 0.05
    n_generations: int = 20
    points_column: str = 'proj'
    population_size: int = 5000
    position_column: str = 'pos'
    salary_column: str = 'salary'
    select_method: str = 'roulette'
    stop_criteria: int = 10
    verbose: bool = True


@dataclass
class PluginSettings:
    driver_managers: Dict[str, Any] = None
    extension_managers: Dict[str, Any] = None


@dataclass
class SiteSettings:
    lineup_size: int = 9
    posfilter: Dict[str, int] = field(default_factory=lambda: {'QB': 14, 'RB': 8, 'WR': 8, 'TE': 5, 'DST': 4, 'FLEX': 8})
    posmap: Dict[str, int] = field(default_factory=lambda: {'DST': 1, 'QB': 1, 'TE': 1, 'RB': 2, 'WR': 3, 'FLEX': 7})
    salary_cap: int = 50000
    flex_positions: Iterable = ('RB', 'WR', 'TE')


@dataclass
class AppSettings:
    ga_settings: GASettings
    site_settings: SiteSettings
    plugin_settings: PluginSettings


def ctx_from_dict(raw_cfg):
    """Creates config object from dictionary"""

    # create and validate the Configuration object
    return dacite.from_dict(
        data_class=AppSettings, 
        data=raw_cfg
    )