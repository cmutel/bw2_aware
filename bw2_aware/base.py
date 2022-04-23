from bw2data import Database, Method
from bw2regional import geocollections
import os
import wrapt

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))


class NoRegionalizedSetup(Exception):
    """First run ``bw2regionalsetup` in this project"""

    pass


@wrapt.decorator
def regionalized_setup(wrapped, instance, args, kwargs):
    if "world" not in geocollections:
        raise NoRegionalizedSetup
    return wrapped(*args, **kwargs)


class LCIA:
    def __init__(self, biosphere="biosphere3"):
        self.db = Database(biosphere)
        self.method = Method(self.name)

    @property
    def metadata(self):
        obj = {
            "unit": self.unit,
            "description": self.description,
            "url": self.url,
            "geocollections": [],
        }
        if self.geocollection:
            obj["geocollections"] = [self.geocollection]
        return obj

    @regionalized_setup
    def import_regional_method(self):
        self.method.register(**self.metadata)
        self.setup_geocollections()
        self.method.write(list(self.regional_cfs()))

    def __repr__(self):
        return str(self.name)
