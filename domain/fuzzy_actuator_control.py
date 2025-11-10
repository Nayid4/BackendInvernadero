from simpful import FuzzySystem, LinguisticVariable, TriangleFuzzySet

class FuzzyActuatorsControl:
    def __init__(self, profile):
        self.profile = profile
        self.FS = FuzzySystem()
        # Temperatura difusa
        self.FS.add_linguistic_variable(
            "temperatura",
            LinguisticVariable([
                TriangleFuzzySet(profile['temp_range'][0], profile['temp_range'][0] + 5, profile['temp_range'][1], term="bajo"),
                TriangleFuzzySet(profile['temp_range'][0] + 5, (profile['temp_range'][1] + profile['temp_range'][0]) / 2, profile['temp_range'][1] - 5, term="medio"),
                TriangleFuzzySet(profile['temp_range'][1] - 5, profile['temp_range'][1], profile['temp_range'][1] + 5, term="alto"),
            ], universe_of_discourse=[profile['temp_range'][0], profile['temp_range'][1] + 5])
        )
        # Humedad aire difusa
        self.FS.add_linguistic_variable(
            "humedad_aire",
            LinguisticVariable([
                TriangleFuzzySet(profile['hum_aire_range'][0], profile['hum_aire_range'][0] + 10, profile['hum_aire_range'][1], term="bajo"),
                TriangleFuzzySet(profile['hum_aire_range'][0] + 10, (profile['hum_aire_range'][1] + profile['hum_aire_range'][0]) / 2, profile['hum_aire_range'][1] - 10, term="medio"),
                TriangleFuzzySet(profile['hum_aire_range'][1] - 10, profile['hum_aire_range'][1], profile['hum_aire_range'][1] + 10, term="alto"),
            ], universe_of_discourse=[profile['hum_aire_range'][0], profile['hum_aire_range'][1] + 10])
        )
        # Humedad suelo difusa
        self.FS.add_linguistic_variable(
            "humedad_suelo",
            LinguisticVariable([
                TriangleFuzzySet(profile['hum_suelo_range'][0], profile['hum_suelo_range'][0] + 10, profile['hum_suelo_range'][1], term="bajo"),
                TriangleFuzzySet(profile['hum_suelo_range'][0] + 10, (profile['hum_suelo_range'][1] + profile['hum_suelo_range'][0]) / 2, profile['hum_suelo_range'][1] - 10, term="medio"),
                TriangleFuzzySet(profile['hum_suelo_range'][1] - 10, profile['hum_suelo_range'][1], profile['hum_suelo_range'][1] + 10, term="alto"),
            ], universe_of_discourse=[profile['hum_suelo_range'][0], profile['hum_suelo_range'][1] + 10])
        )
        # Variables de salida (actuador)
        self.FS.add_linguistic_variable(
            "ventilador",
            LinguisticVariable([
                TriangleFuzzySet(0, 0, 1, term="bajo"),
                TriangleFuzzySet(0, 1, 1, term="alto")
            ], universe_of_discourse=[0, 1])
        )
        self.FS.add_linguistic_variable(
            "bomba",
            LinguisticVariable([
                TriangleFuzzySet(0, 0, 1, term="bajo"),
                TriangleFuzzySet(0, 1, 1, term="alto")
            ], universe_of_discourse=[0, 1])
        )
        self.FS.add_linguistic_variable(
            "luz",
            LinguisticVariable([
                TriangleFuzzySet(0, 0, 1, term="bajo"),
                TriangleFuzzySet(0, 1, 1, term="alto")
            ], universe_of_discourse=[0, 1])
        )
        # Reglas
        self.FS.add_rules([
            "IF (temperatura IS alto) THEN (ventilador IS alto)",
            "IF (temperatura IS medio) THEN (ventilador IS medio)",
            "IF (temperatura IS bajo) THEN (ventilador IS bajo)",
            "IF (humedad_suelo IS bajo) THEN (bomba IS alto)",
            "IF (humedad_suelo IS medio) THEN (bomba IS medio)",
            "IF (humedad_suelo IS alto) THEN (bomba IS bajo)",
            "IF (humedad_aire IS bajo) THEN (ventilador IS alto)"
        ])

    def clasificar_nivel(self, valor, rangos):
        bajo, alto = rangos
        if valor <= bajo:
            return "bajo"
        elif valor >= alto:
            return "alto"
        else:
            return "medio"

    def decidir(self, temperatura, humedad_aire, humedad_suelo):
        self.FS.set_variable("temperatura", temperatura)
        self.FS.set_variable("humedad_aire", humedad_aire)
        self.FS.set_variable("humedad_suelo", humedad_suelo)
        output = self.FS.inference()
        temp_nivel = self.clasificar_nivel(temperatura, self.profile['temp_range'])
        hum_aire_nivel = self.clasificar_nivel(humedad_aire, self.profile['hum_aire_range'])
        hum_suelo_nivel = self.clasificar_nivel(humedad_suelo, self.profile['hum_suelo_range'])
        recomendacion = self.buscar_recomendacion(temp_nivel, hum_aire_nivel, hum_suelo_nivel)
        return {
            "ventilador": output.get('ventilador', 'bajo'),
            "bomba": output.get('bomba', 'bajo'),
            "luz": output.get('luz', 'bajo'),
            "recomendacion": recomendacion,
            "centroide": self.profile['centroide']
        }

    def buscar_recomendacion(self, temp_nivel, hum_aire_nivel, hum_suelo_nivel):
        for rule in self.profile['rules']:
            if (rule['temperatura_nivel'] == temp_nivel and
                rule['humedad_aire_nivel'] == hum_aire_nivel and
                rule['humedad_suelo_nivel'] == hum_suelo_nivel):
                return rule['recomendacion']
        return "Condición no reconocida, consulta manual recomendada."
