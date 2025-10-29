from simpful import FuzzySystem, LinguisticVariable, TriangleFuzzySet

class ControlAbanicoSimpful:
    def __init__(self):
        self.FS = FuzzySystem()
        self.FS.add_linguistic_variable("temperatura",
            LinguisticVariable([
                TriangleFuzzySet(20, 25, 30, term="bajo"),
                TriangleFuzzySet(28, 35, 50, term="alto")
            ], universe_of_discourse=[15,55]))
        self.FS.add_linguistic_variable("humedad_ambiental",
            LinguisticVariable([
                TriangleFuzzySet(20, 40, 60, term="seco"),
                TriangleFuzzySet(55, 75, 95, term="humedo")
            ], universe_of_discourse=[0,100]))
        self.FS.add_linguistic_variable("humedad_suelo",
            LinguisticVariable([
                TriangleFuzzySet(500, 1500, 4000, term="seco"),
                TriangleFuzzySet(3500, 4095, 4095, term="humedo")
            ], universe_of_discourse=[0,4095]))
        self.FS.add_linguistic_variable("fan",
            LinguisticVariable([
                TriangleFuzzySet(0, 0, 1, term="off"),
                TriangleFuzzySet(0, 1, 1, term="on")
            ], universe_of_discourse=[0,1]))
        # Ajusta reglas según lo ambiental, se pueden ampliar
        self.FS.add_rules([
            "IF (temperatura IS alto) AND (humedad_ambiental IS seco) THEN (fan IS on)",
            "IF (temperatura IS alto) AND (humedad_ambiental IS humedo) THEN (fan IS off)",
            "IF (temperatura IS bajo) AND (humedad_suelo IS humedo) THEN (fan IS off)",
            "IF (temperatura IS alto) AND (humedad_suelo IS seco) THEN (fan IS on)"
        ])


    def decidir(self, temperatura, humedad_ambiental, humedad_suelo):
        self.FS.set_variable("temperatura", temperatura)
        self.FS.set_variable("humedad_ambiental", humedad_ambiental)
        self.FS.set_variable("humedad_suelo", humedad_suelo)
        output = self.FS.inference()
        return output['fan'] > 0.5
