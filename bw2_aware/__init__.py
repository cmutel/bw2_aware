__all__ = ("import_aware", "AnnualAgricultural", "AnnualNonagricultural")

__version__ = (0, 2, 1)

from .aware import AnnualAgricultural, AnnualNonagricultural
from bw2regional.pandarus_remote import remote, AlreadyExists


METHODS = (AnnualAgricultural, AnnualNonagricultural)


def import_aware(biosphere="biosphere3"):
    for method in METHODS:
        try:
            method(biosphere).import_regional_method()
        except NotImplemented:
            pass

    try:
        job = remote.calculate_intersection("world", "watersheds-aware")
        job.poll(interval=2)
        if job.status != "finished":
            raise ValueError(
                "Calculation job finished with status '{}'".format(job.status)
            )
    except AlreadyExists:
        pass
    remote.intersection_as_new_geocollection(
        "world", "watersheds-aware", "world-topo-watersheds-aware"
    )
    try:
        job = remote.calculate_intersection(
            "world-topo-watersheds-aware", "watersheds-aware"
        )
        job.poll(interval=2)
        if job.status != "finished":
            raise ValueError(
                "Calculation job finished with status '{}'".format(job.status)
            )
    except AlreadyExists:
        pass
    remote.intersection("world-topo-watersheds-aware", "watersheds-aware")
