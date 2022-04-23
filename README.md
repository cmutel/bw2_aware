# AWARE regionalized LCIA method for Brightway

This package provides the [AWARE](http://www.wulca-waterlca.org/aware.html) regionalized LCIA method in [brightway](https://brightway.dev>) and [brightway2-regional](https://github.com/brightway-lca/brightway2-regional).

Monthly characterization factors are currently not imported.

## Installation

As this package requires `bw2regional`, we recommend installation via conda.

## Usage

You should be in a project that has the `biosphere3` base biosphere data installed.

```python
import bw2_aware, bw2regional
bw2regional.create_world_collections()
bw2_aware.import_regionalized_aware()
```

The following methods are now available to be used as (either regionalized or site-generic LCIA methods):

* ('AWARE', '1.2 (April 2017)', 'Annual', 'Agricultural')
* ('AWARE', '1.2 (April 2017)', 'Annual', 'Non-agricultural')
