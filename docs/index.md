pangadfs is a pandas-based (python) genetic algorithm framework for fantasy sports. It uses a plugin architecture to enable maximum flexibility while also providing a fully-functional implementation of a genetic algorithm for lineup optimization.

pangadfs-configapp is a plugin that provides for structured configuration of pangadfs applications. Specifically, it offers an OptimizeConfig in the pangadfs.optimize namespace to coordinate the steps of lineup optimization using an AppSettings object.

---

**Documentation**: <a href="https://sansbacon.github.io/pangadfs-configapp/">https://sansbacon.github.io/pangadfs-configapp/</a>

**Source Code**: <a href="https://github.com/sansbacon/pangadfs-configapp" target="_blank">https://github.com/sansbacon/pangadfs-configapp</a>

---

The key pangadfs-configapp feature is that it uses python dataclasses to provide structured configuration for pangadfs apps. The basic app example in pangadfs uses a dictionary, which is not as robust because it does not require certain keys to be present and that they have specific types. Pangadfs-configapp uses the dacite library to create a configuration object from an ordinary dictionary while supplying sensible defaults for all missing values.


## Requirements

* Python 3.8+
* dacite 1.0+


## Installation

<div class="termy">

```console
$ pip install pangadfs-configapp

```

</div>

## Example

### Create It

An optimizer app using pangadfs-configapp could look like the following

```Python
import json
from pathlib import Path

from stevedore.driver import DriverManager 
from stevedore.named import NamedExtensionManager

from pangadfs.ga import GeneticAlgorithm
from pangadfs_configapp.gasettings import ctx_from_dict


# setup configuration
DATADIR = Path(__file__).parent / 'appdata'
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
```

### Run it

Run the sample application with:

<div class="termy">

```console
$ python pangadfs_configapp/app/app.py

INFO:root:Starting generation 1
INFO:root:Best lineup score 153.00000000000003
INFO:root:Lineup unimproved 1 times
INFO:root:Starting generation 2
INFO:root:Best lineup score 153.00000000000003
INFO:root:Lineup improved to 155.2
. . . 
INFO:root:Starting generation 19
INFO:root:Best lineup score 156.3
INFO:root:Lineup improved to 156.5
INFO:root:Starting generation 20
INFO:root:Best lineup score 156.5
INFO:root:Lineup unimproved 1 times

               player team  pos  salary  proj
0             Saints    NO  DST    3800   9.8
34    Patrick Mahomes   KC   QB    8000  26.6
62        Dalvin Cook  MIN   RB    9500  27.2
68       Nyheim Hines  IND   RB    4600  15.9
72         Brian Hill  ATL   RB    4000  12.8
109     Gabriel Davis  BUF   WR    3000  10.7
136   Keelan Cole Sr.  JAX   WR    3600  11.9
138     Calvin Ridley  ATL   WR    7100  21.6
142  Justin Jefferson  MIN   WR    6300  20.0
Lineup score: 156.5
```
</div>

## License

This project is licensed under the terms of the MIT license.