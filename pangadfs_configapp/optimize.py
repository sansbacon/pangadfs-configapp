# pangadfs_configapp/optimize.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

import logging
from typing import Any, Dict

import numpy as np

from pangadfs.ga import GeneticAlgorithm
from pangadfs.optimize import OptimizeDefault


class OptimizeConfig(OptimizeDefault):


    def optimize(self, 
                 *,
                 ga: GeneticAlgorithm,
                 **kwargs
                ) -> Dict[str, Any]:
        """Creates initial pool
        
        Args:
            ga (GeneticAlgorithm): the GeneticAlgorithm instance,
            **kwargs: keyword arguments for plugins
            
        Returns:
            Dict
            'population': np.ndarray,
            'fitness': np.ndarray,
            'best_lineup': pd.DataFrame,
            'best_score': float

        """
        pop_size = ga.ctx.ga_settings.population_size
        pool = ga.pool(csvpth=ga.ctx.ga_settings.csvpth)
        cmap = {'points': ga.ctx.ga_settings.points_column,
			    'position': ga.ctx.ga_settings.position_column,
			    'salary': ga.ctx.ga_settings.salary_column}
        posfilter = ga.ctx.site_settings.posfilter
        pospool = ga.pospool(
            pool=pool, 
            posfilter=posfilter, 
            column_mapping=cmap, 
            flex_positions=ga.ctx.site_settings.flex_positions
        )

        # create dict of index and stat value
        # this will allow easy lookup later on
        cmap = {'points': ga.ctx.ga_settings.points_column,
                'salary': ga.ctx.ga_settings.salary_column}
        points = pool[cmap['points']].values
        salaries = pool[cmap['salary']].values
        
        # CREATE INITIAL POPULATION
        initial_population = ga.populate(
            pospool=pospool, 
            posmap=ga.ctx.site_settings.posmap, 
            population_size=pop_size
        )

        # apply validators
        initial_population = ga.validate(
            population=initial_population, 
            salaries=salaries,
            salary_cap=ga.ctx.site_settings.salary_cap
        )

        population_fitness = ga.fitness(
            population=initial_population, 
            points=points
        )

        # set overall_max based on initial population
        omidx = population_fitness.argmax()
        best_fitness = population_fitness[omidx]
        best_lineup = initial_population[omidx]
        population = initial_population.copy()

        # CREATE NEW GENERATIONS
        n_unimproved = 0
        for i in range(1, ga.ctx.ga_settings.n_generations + 1):
            if n_unimproved == ga.ctx.ga_settings.stop_criteria:
                break

            if ga.ctx.ga_settings.verbose:
                logging.info(f'Starting generation {i}')
                logging.info(f'Best lineup score {best_fitness}')

            elite = ga.select(
                population=population, 
                population_fitness=population_fitness, 
                n=len(population) // ga.ctx.ga_settings.elite_divisor,
                method=ga.ctx.ga_settings.elite_method
            )

            selected = ga.select(
                population=population, 
                population_fitness=population_fitness, 
                n=len(population),
                method=ga.ctx.ga_settings.select_method
            )

            # crossover
            crossed_over = ga.crossover(
                population=selected, 
                method=ga.ctx.ga_settings.crossover_method
            )

            # mutation
            mutated = ga.mutate(population=crossed_over, mutation_rate=ga.ctx.ga_settings.mutation_rate)

            # validation
            population = ga.validate(
                population=np.vstack((elite, mutated)), 
                salaries=salaries, 
                salary_cap=ga.ctx.site_settings.salary_cap
            )
            
            # get fitness and compare to prior solutions
            population_fitness = ga.fitness(population=population, points=points)
            omidx = population_fitness.argmax()
            generation_max = population_fitness[omidx]
        
            if generation_max > best_fitness:
                if ga.ctx.ga_settings.verbose:
                    logging.info(f'Lineup improved to {generation_max}')
                best_fitness = generation_max
                best_lineup = population[omidx]
                n_unimproved = 0
            else:
                n_unimproved += 1
                if ga.ctx.ga_settings.verbose:
                    logging.info(f'Lineup unimproved {n_unimproved} times')


        # FINALIZE RESULTS
        # will break after n_generations or when stop_criteria reached
        return {
            'population': population,
            'fitness': population_fitness,
            'best_lineup': pool.loc[best_lineup, :],
            'best_score': best_fitness
        }
