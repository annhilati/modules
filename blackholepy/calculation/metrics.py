from wolframclient.language import wl

x = wl.Symbol("x")
y = wl.Symbol("y")
z = wl.Symbol("z")

class BlackHoleMetric():
    """Class representing a set of formulas rigarding properties of black holes, result from a solution to the Einstein field equations and are true under certain circumstances."""
    
    name:                str
    r_plus:              wl.Equal
    r_minus:             Equality | None
    surface_gravity:     Equality
    horizon_area:        Equality
    hawking_temperature: Equality
    hawking_power:       Equality
    evaporation_time:    Equality

    def __repr__(self):
        return f"<BlackHoleMetric '{self.name}'>"
    
    def __str__(self):
        return self.name