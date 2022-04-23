__all__ = (
    "import_global_aware",
    "import_regionalized_aware",
    "create_regionalized_intersections",
)


__version__ = (0, 3)

from .aware import AnnualAgricultural, AnnualNonagricultural
from bw2regional.pandarus_remote import remote, AlreadyExists


METHODS = (AnnualAgricultural, AnnualNonagricultural)



def import_global_aware(biosphere="biosphere3"):
    raise NotImplementedError("This package only provide regionalized CFs")


def import_regionalized_aware(biosphere="biosphere3"):
    for method in METHODS:
        method(biosphere).import_regional_method()


def create_regionalized_intersections():
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
