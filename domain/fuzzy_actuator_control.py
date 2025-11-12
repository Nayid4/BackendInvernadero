from simpful import FuzzySystem, LinguisticVariable, TriangleFuzzySet

CRISP = {
    "Lechuga": {
        "temp_range": (22, 26),
        "hum_suelo_range": (60, 80),
        "hum_aire_range": (60, 80),
        "luz_range": (40, 60)
    },
    "Tomate": {
        "temp_range": (24, 30),
        "hum_suelo_range": (50, 70),
        "hum_aire_range": (50, 70),
        "luz_range": (65, 90)
    },
    "Pimenton": {
        "temp_range": (24, 32),
        "hum_suelo_range": (50, 70),
        "hum_aire_range": (50, 70),
        "luz_range": (60, 85)
    }
}

class FuzzyActuatorsControl:
    def __init__(self,  crisp):
        # Temperatura -> Ventilador (1/2/3)
        self.FS_temp_vent = FuzzySystem()
        tmin, tmax = crisp['temp_range']
        self.FS_temp_vent.add_linguistic_variable(
            "temperatura",
            LinguisticVariable([
                TriangleFuzzySet(0, tmin, (tmin + tmax) / 2, term="bajo"),
                TriangleFuzzySet(tmin, (tmin + tmax) / 2, tmax, term="medio"),
                TriangleFuzzySet((tmin + tmax) / 2, tmax, 100, term="alto"),
            ], universe_of_discourse=[0, 100])
        )
        self.FS_temp_vent.add_linguistic_variable(
            "ventilador",
            LinguisticVariable([
                TriangleFuzzySet(1, 1, 2, term="bajo"),
                TriangleFuzzySet(1, 2, 3, term="medio"),
                TriangleFuzzySet(2, 3, 3, term="alto"),
            ], universe_of_discourse=[1, 3])
        )
        self.FS_temp_vent.add_rules([
            "IF (temperatura IS bajo) THEN (ventilador IS bajo)",
            "IF (temperatura IS medio) THEN (ventilador IS medio)",
            "IF (temperatura IS alto) THEN (ventilador IS alto)"
        ])

        # Humedad del suelo -> Rociador (30/60/90)
        self.FS_humsuelo_bomba = FuzzySystem()
        smn, smx = crisp['hum_suelo_range']
        self.FS_humsuelo_bomba.add_linguistic_variable(
            "humedad_suelo",
            LinguisticVariable([
                TriangleFuzzySet(0, smn, (smn + smx) / 2, term="bajo"),
                TriangleFuzzySet(smn, (smn + smx) / 2, smx, term="medio"),
                TriangleFuzzySet((smn + smx) / 2, smx, 4095, term="alto")
            ], universe_of_discourse=[0, 4095])
        )
        self.FS_humsuelo_bomba.add_linguistic_variable(
            "rociador",
            LinguisticVariable([
                TriangleFuzzySet(30, 30, 60, term="corto"),
                TriangleFuzzySet(30, 60, 90, term="medio"),
                TriangleFuzzySet(60, 90, 90, term="largo"),
            ], universe_of_discourse=[30, 90])
        )
        self.FS_humsuelo_bomba.add_rules([
            "IF (humedad_suelo IS bajo) THEN (rociador IS largo)",
            "IF (humedad_suelo IS medio) THEN (rociador IS medio)",
            "IF (humedad_suelo IS alto) THEN (rociador IS corto)"
        ])

        # Humedad aire -> Luminosidad (1/2/3)
        self.FS_humaire_luz = FuzzySystem()
        amin, amax = crisp['hum_aire_range']
        self.FS_humaire_luz.add_linguistic_variable(
            "humedad_aire",
            LinguisticVariable([
                TriangleFuzzySet(0, amin, (amin + amax) / 2, term="bajo"),
                TriangleFuzzySet(amin, (amin + amax) / 2, amax, term="medio"),
                TriangleFuzzySet((amin + amax) / 2, amax, 100, term="alto"),
            ], universe_of_discourse=[0, 100])
        )
        self.FS_humaire_luz.add_linguistic_variable(
            "luminosidad",
            LinguisticVariable([
                TriangleFuzzySet(1, 1, 2, term="bajo"),
                TriangleFuzzySet(1, 2, 3, term="medio"),
                TriangleFuzzySet(2, 3, 3, term="alto"),
            ], universe_of_discourse=[1, 3])
        )
        self.FS_humaire_luz.add_rules([
            "IF (humedad_aire IS bajo) THEN (luminosidad IS alto)",
            "IF (humedad_aire IS medio) THEN (luminosidad IS medio)",
            "IF (humedad_aire IS alto) THEN (luminosidad IS bajo)"
        ])

        self.crisp = crisp

    def discretizar(self, salida, permitidos):
        v = int(round(salida))
        return min(permitidos, key=lambda x: abs(x - v))

    def decidir(self, temperatura, humedad_aire, humedad_suelo):
        result = {}

        # 1. Temperatura -> Ventilador
        tmin, tmax = self.crisp['temp_range']
        if tmin <= temperatura <= tmax:
            result['ventilador'] = 0
        else:
            out_vent = self.FS_temp_vent.set_variable("temperatura", temperatura)
            s = self.FS_temp_vent.inference()["ventilador"]
            result['ventilador'] = self.discretizar(s, [1, 2, 3])

        # 2. Humedad suelo -> Rociador
        smn, smx = self.crisp['hum_suelo_range']
        if smn <= humedad_suelo <= smx:
            result['rociador'] = 0
        else:
            self.FS_humsuelo_bomba.set_variable("humedad_suelo", humedad_suelo)
            s = self.FS_humsuelo_bomba.inference()["rociador"]
            result['rociador'] = self.discretizar(s, [30, 60, 90])

        # 3. Humedad aire -> Luminosidad
        amin, amax = self.crisp['hum_aire_range']
        if amin <= humedad_aire <= amax:
            result['luminosidad'] = 0
        else:
            self.FS_humaire_luz.set_variable("humedad_aire", humedad_aire)
            s = self.FS_humaire_luz.inference()["luminosidad"]
            result['luminosidad'] = self.discretizar(s, [1, 2, 3])

        return result
