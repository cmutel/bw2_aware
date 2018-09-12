from .base import LCIA, data_dir, fiona, geocollections
import os


SURFACE_WATER = [
    ('Fresh water (obsolete)', ('water', 'surface water')),
    ('Water', ('water',)),
    ('Water', ('water', 'surface water')),
    ('Water, cooling, unspecified natural origin', ('natural resource', 'in water')),
    ('Water, lake', ('natural resource', 'in water')),
    ('Water, river', ('natural resource', 'in water')),
    ('Water, turbine use, unspecified natural origin', ('natural resource', 'in water')),
    ('Water, unspecified natural origin', ('natural resource', 'in water')),
]

GROUND_WATER = [
    ('Water', ('water', 'ground-')),
    ('Water', ('water', 'ground-, long-term')),
    ('Water, unspecified natural origin', ('natural resource', 'in ground')),
    ('Water, well, in ground', ('natural resource', 'in water')),
]


class AWARE(LCIA):
    vector_ds = os.path.join(data_dir, "aware.gpkg")
    geocollection = 'watersheds-aware'
    unit = "Availability Minus Demand (AMD), m**3/m**2/month"
    description = """AWARE is a water use midpoint indicator representing the relative Available WAter REmaining per area in a watershed, after the demand of humans and aquatic ecosystems has been met. It assesses the potential of water deprivation, to either humans or ecosystems, building on the assumption that the less water remaining available per area, the more likely another user will be deprived.

    It is first calculated as the water Availability Minus the Demand (AMD) of humans and aquatic ecosystems and is relative to the area (m3 m-2 month-1). In a second step, the value is normalized with the world average result (AMD = 0.0136m3m-2 month-1) and inverted, and hence represents the relative value in comparison with the average m3 consumed in the world (the world average is calculated as a consumption-weighted average). Once inverted, 1/AMD  can be interpreted as a surface-time equivalent to generate unused water in this region. The indicator is limited to a range from 0.1 to 100, with a value of 1 corresponding to the world average, and a value of 10, for example, representing a region where there is 10 times less available water remaining per area than the world average."""
    url = "http://www.wulca-waterlca.org/aware.html"

    def _water_flows(self, kind='all'):
        mapping = {
            'all': SURFACE_WATER + GROUND_WATER,
            'surface': SURFACE_WATER,
            'ground': GROUND_WATER
        }
        flows = mapping[kind]

        for act in self.db:
            name, categories = act['name'], tuple(act['categories'])
            for x, y in flows:
                if name == x and categories == y:
                    yield act.key

    def setup_geocollections(self):
        if self.geocollection not in geocollections:
            geocollections[self.geocollection] = {
                'filepath': self.vector_ds,
                'field': self.id_column,
            }

    def global_cfs(self):
        for key in self._water_flows():
            yield((key, self.global_cf, "GLO"))

    @regionalized
    def regional_cfs(self):
        water_flows = list(self._water_flows())

        for obj in self.global_cfs():
            yield obj

        with fiona.drivers():
            with fiona.open(self.vector_ds) as src:
                for feat in src:
                    for key in water_flows:
                        yield (
                            key,
                            feat['properties'][self.column],
                            (self.geocollection, feat['properties'][self.id_column])
                        )


class AnnualAgricultural(AWARE):
    column = 'HH'
    name = ("AWARE", "1.2 (April 2017)", "Water Use", "Human Health", "Marginal")
    global_cf =
    id_column =
