# AWARE regionalized LCIA method for Brightway2

This package provides the [AWARE](http://www.wulca-waterlca.org/aware.html) regionalized LCIA method in [brightway2](https://brightwaylca.org>) and [brightway2-regional](https://bitbucket.org/cmutel/brightway2-regional).

Monthly characterization factors are currently not imported.

## Installation

`pip install bw2_aware`

Requires `bw2regional`.

## Usage

You should be in a project that has the `biosphere3` base biosphere data installed.

```python
import bw2_aware, bw2regional
bw2regional.bw2regionalsetup()
bw2_aware.import_aware()
```

The following methods are now available to be used as (either regionalized or site-generic LCIA methods):

* ('AWARE', '1.2 (April 2017)', 'Annual', 'Agricultural')
* ('AWARE', '1.2 (April 2017)', 'Annual', 'Non-agricultural')
