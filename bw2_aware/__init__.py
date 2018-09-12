__all__ = (
    'import_aware',
)

__version__ = (0, 1)

from .water import (
    WaterHumanHealthMarginal,
    WaterHumanHealthAverage,
)
from .base import remote

METHODS = (
    WaterHumanHealthMarginal,
    WaterEcosystemQualityCertain,
)


def import_aware(biosphere='biosphere3'):
    for method in METHODS:
        try:
            method(biosphere).import_regional_method()
        except NotImplemented:
            pass

    try:
        remote.intersection("world", "watersheds-aware")
        remote.intersection_as_new_geocollection(
            'world',
            'watersheds-aware',
            'world-topo-watersheds-hh'
        )
    except:
        print("Can't import data from pandarus remote")

