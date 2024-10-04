MAIN_SOILMAP_UNITS = ["peat", "moerig", "buried", "other"]
MAIN_BGT_UNITS = [
    "pand",  # Panden
    "wegdeel",  # Wegen
    "waterdeel",  # Grote wateren
    "ondersteunendwegdeel",  # Overig
    "ondersteunendwaterdeel",  # Overig
    "begroeidterreindeel",  # Percelen, Natuur
    "onbegroeidterreindeel",  # Erven, Functioneel gebied
    "scheiding",  # Overig
    "overigbouwwerk",  # Panden
]

EMISSION_FACTORS = { # ton / ha
    "pand_peat": 10.25,
    "wegdeel_peat": 10.25,
    "waterdeel_peat": 0.0,
    "ondersteunendwegdeel_peat": 10.25,
    "ondersteunendwaterdeel_peat": 10.25,
    "begroeidterreindeel_peat": 10.25,
    "onbegroeidterreindeel_peat": 10.25,
    "scheiding_peat": 10.25,
    "overigbouwwerk_peat": 10.25,
    "pand_moerig": 12.36,
    "wegdeel_moerig": 12.36,
    "waterdeel_moerig": 0.0,
    "ondersteunendwegdeel_moerig": 12.36,
    "ondersteunendwaterdeel_moerig": 12.36,
    "begroeidterreindeel_moerig": 12.36,
    "onbegroeidterreindeel_moerig": 12.36,
    "scheiding_moerig": 12.36,
    "overigbouwwerk_moerig": 12.36,
    "pand_buried": 0.0,
    "wegdeel_buried": 0.0,
    "waterdeel_buried": 0.0,
    "ondersteunendwegdeel_buried": 0.0,
    "ondersteunendwaterdeel_buried": 0.0,
    "begroeidterreindeel_buried": 0.0,
    "onbegroeidterreindeel_buried": 0.0,
    "scheiding_buried": 0.0,
    "overigbouwwerk_buried": 0.0,
    "pand_other": 0.0,
    "wegdeel_other": 0.0,
    "waterdeel_other": 0.0,
    "ondersteunendwegdeel_other": 0.0,
    "ondersteunendwaterdeel_other": 0.0,
    "begroeidterreindeel_other": 0.0,
    "onbegroeidterreindeel_other": 0.0,
    "scheiding_other": 0.0,
    "overigbouwwerk_other": 0.0,
}