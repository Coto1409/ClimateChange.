import unicodedata
from flask import Flask, render_template, request

app = Flask(__name__)

prompt_responses = {
    "qué es el cambio climático": "El cambio climático es la variación del clima global causada principalmente por actividades humanas y emisiones de gases de efecto invernadero.",
    "cómo impacta el calentamiento global al planeta": "El calentamiento global aumenta temperaturas, altera patrones de lluvia, reduce hielo polar y eleva el nivel del mar.",
    "cuáles son los gases de efecto invernadero más importantes": "Los gases más importantes son dióxido de carbono, metano, óxidos de nitrógeno y vapor de agua.",
    "por qué es importante reducir las emisiones de carbono": "Reducir emisiones de carbono ayuda a limitar el calentamiento global y a proteger ecosistemas y salud humana.",
    "cómo ayuda la energía renovable a combatir el cambio climático": "La energía renovable genera electricidad sin quemar combustibles fósiles, reduciendo emisiones y contaminación.",
    "qué consecuencias tiene la deforestación en el clima": "La deforestación libera carbono y reduce la capacidad del planeta para absorber CO2, agravando el cambio climático.",
    "cómo se relaciona el reciclaje con la protección del clima": "Reciclar reduce la necesidad de extraer y procesar materiales nuevos, lo que disminuye emisiones y residuos.",
    "qué papel tiene el agua en el cambio climático": "El agua regula el clima y su disponibilidad se ve afectada por sequías, inundaciones y cambios en el ciclo hidrológico.",
    "qué causa la sequía en el contexto climático": "La sequía puede ser causada por menos precipitaciones y temperaturas más altas, afectando agricultura y reservas de agua.",
    "cómo aumentan las inundaciones por el cambio climático": "El aire más cálido retiene más humedad, lo que puede provocar lluvias intensas e inundaciones más frecuentes.",
    "qué significa el deshielo polar": "El deshielo polar es el derretimiento de hielo en glaciares y casquetes, contribuyendo a la subida del nivel del mar.",
    "cómo afectan los océanos al calentamiento global": "Los océanos absorben calor y CO2, pero se calientan y acidifican, lo que daña la vida marina y regula el clima.",
    "por qué es clave preservar la biodiversidad": "La biodiversidad mantiene ecosistemas equilibrados y resistentes, fundamentales para la estabilidad climática.",
    "cómo daña la contaminación al medio ambiente": "La contaminación del aire, agua y suelo reduce la calidad de vida y agrava los efectos del cambio climático.",
    "qué es la huella de carbono personal": "La huella de carbono personal mide los gases de efecto invernadero generados por nuestras actividades diarias.",
    "cómo reduce el transporte sostenible las emisiones": "El transporte sostenible reduce el uso de combustibles fósiles mediante medios más eficientes y menos contaminantes.",
    "qué beneficios tienen los autos eléctricos": "Los autos eléctricos generan pocas emisiones directas y son más sostenibles si se cargan con energía renovable.",
    "cómo afectan los plásticos al clima": "La producción y eliminación de plásticos generan emisiones y contaminan el aire, suelos y océanos.",
    "qué significa consumo responsable": "El consumo responsable implica elegir productos duraderos, eficientes y con menor impacto ambiental.",
    "qué es la economía verde": "La economía verde promueve crecimiento económico con menor daño ambiental y uso sostenible de recursos.",
    "cómo se aplica la agricultura sostenible": "La agricultura sostenible utiliza prácticas que conservan el suelo, el agua y reducen emisiones de gases de efecto invernadero.",
    "qué impacto tiene el consumo de carne en el clima": "La producción de carne requiere mucha agua y tierra, y genera emisiones significativas de metano.",
    "qué es la política climática": "La política climática son medidas públicas y privadas para reducir emisiones y adaptarse a los efectos del cambio climático.",
    "qué es el acuerdo de parís": "El Acuerdo de París es un tratado internacional para limitar el calentamiento global a menos de 2 °C y acercarse a 1.5 °C.",
    "qué es la adaptación climática": "La adaptación climática son acciones para ajustar ciudades, agricultura y comunidades a condiciones climáticas cambiantes.",
    "qué es la mitigación climática": "La mitigación climática busca reducir causas del cambio climático mediante energía limpia y eficiencia energética.",
    "cómo contribuye la conservación al clima": "La conservación protege bosques y ecosistemas que almacenan carbono y regulan el clima.",
    "por qué los bosques son importantes para el clima": "Los bosques capturan carbono, generan oxígeno y mantienen la estabilidad del ciclo del agua.",
    "qué es la eficiencia energética": "La eficiencia energética implica usar menos energía para el mismo servicio, reduciendo consumo y emisiones.",
    "qué es la movilidad sostenible": "La movilidad sostenible incluye caminar, bicicleta y transporte público con menor impacto ambiental.",
    "cómo funciona el compostaje": "El compostaje transforma residuos orgánicos en abono, reduciendo basura y emisiones de metano.",
    "qué significa reutilizar materiales": "Reutilizar materiales prolonga su vida útil y reduce la necesidad de fabricar productos nuevos.",
    "por qué es importante reducir residuos": "Reducir residuos evita contaminación, ahorro recursos y disminuye la huella ambiental.",
    "qué es la educación ambiental": "La educación ambiental enseña a entender el clima y a tomar decisiones sostenibles.",
    "qué papel juegan los jóvenes en la acción climática": "Los jóvenes impulsan cambios, generan conciencia y exigen políticas más ambiciosas.",
    "cómo pueden ayudar las comunidades locales al clima": "Las comunidades locales pueden plantar árboles, separar residuos y promover prácticas sostenibles.",
    "cómo impacta el cambio climático en la salud humana": "El cambio climático aumenta el riesgo de enfermedades, olas de calor y problemas respiratorios.",
    "por qué es importante cuidar el planeta": "Cuidar el planeta protege la vida actual y garantiza recursos para las futuras generaciones.",
    "qué significa un futuro sostenible": "Un futuro sostenible equilibra desarrollo social, económico y ambiental para el bienestar de todos.",
    "cómo protege la naturaleza el clima": "Los ecosistemas saludables regulan el clima y proporcionan agua, aire y alimento limpios.",
    "qué son los huertos urbanos": "Los huertos urbanos producen alimentos locales, mejoran la calidad del aire y fomentan la sostenibilidad.",
    "por qué usar transporte público ayuda al clima": "El transporte público reduce el número de autos y las emisiones por persona.",
    "cómo conservar el agua en casa": "Conservar agua en casa significa reparar fugas, usar menos agua y reutilizar cuando sea posible.",
    "qué es la responsabilidad climática": "La responsabilidad climática implica acciones individuales y colectivas para reducir el impacto ambiental.",
    "qué es la energía hidroeléctrica": "La energía hidroeléctrica genera electricidad a partir del agua, con menos emisiones directas que los combustibles fósiles.",
    "qué es la economía circular": "La economía circular busca mantener materiales en uso y reducir residuos mediante reciclaje y reutilización.",
    "qué es la movilidad eléctrica": "La movilidad eléctrica utiliza vehículos que funcionan con electricidad en lugar de combustibles fósiles.",
    "qué es el desarrollo sostenible": "El desarrollo sostenible satisface necesidades presentes sin comprometer la capacidad de las futuras generaciones.",
    "qué son las ciudades verdes": "Las ciudades verdes integran espacios naturales, transporte limpio y construcción eficiente para ser más sostenibles.",
    "qué significa la huella hídrica": "La huella hídrica mide el agua utilizada para producir productos, alimentos y servicios.",
    "qué son las acciones locales para el clima": "Las acciones locales incluyen plantar árboles, reducir consumo y educar a la comunidad sobre sostenibilidad.",
    "qué es la energía térmica renovable": "La energía térmica renovable utiliza calor de fuentes limpias como la geotermia o el sol para generar energía.",
    "qué papel tiene la innovación en soluciones climáticas": "La innovación permite tecnologías nuevas para reducir emisiones y adaptarse a un clima cambiante.",
    "cómo afecta la polución al cambio climático": "La polución contribuye al calentamiento global y empeora la calidad del aire, la salud y los ecosistemas.",
    "qué estudia la meteorología en relación con el cambio climático": "La meteorología analiza patrones del tiempo que ayudan a comprender y predecir impactos del cambio climático.",
    "por qué son importantes los ecosistemas sanos": "Los ecosistemas sanos almacenan carbono, regulan el clima y sostienen la vida en el planeta.",
    "qué son los eventos extremos asociados al clima": "Los eventos extremos son huracanes, incendios y olas de calor que aumentan con el calentamiento global.",
    "qué es la educación climática": "La educación climática empodera a las personas a tomar decisiones responsables y a promover la sostenibilidad.",
}


def normalize_text(text):
    text = text.strip().lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')
    text = ''.join(ch for ch in text if ch.isalnum() or ch.isspace())
    return ' '.join(text.split())

prompt_responses_normalized = {
    normalize_text(k): v for k, v in prompt_responses.items()
}

# PAGINA PRINCIPAL

@app.route("/")
def inicio():
    return render_template("index.html")


# CALCULADORA

@app.route("/calculadora", methods=["GET", "POST"])
def calculadora():

    consumo = None
    mensaje = ""

    if request.method == "POST":

        focos = int(request.form["focos"])
        tv = int(request.form["tv"])
        electro = int(request.form["electro"])

        consumo = focos * 5 + tv * 10 + electro * 8

        if consumo < 50:
            mensaje = "Consumo bajo. Buen uso de energía."
        elif consumo < 100:
            mensaje = "Consumo moderado. Puedes mejorar."
        else:
            mensaje = "Consumo alto. Intenta ahorrar energía."

    return render_template(
        "calculadora.html",
        consumo=consumo,
        mensaje=mensaje
    )


# CHATBOT

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    respuesta = ""
    prompts = list(prompt_responses.keys())

    if request.method == "POST":

        pregunta = normalize_text(request.form["pregunta"])
        respuesta = prompt_responses_normalized.get(
            pregunta,
            "Lo siento, no entiendo la pregunta. Usa uno de los 50 prompts profesionales mostrados en la página."
        )

    return render_template(
        "chatbot.html",
        respuesta=respuesta,
        prompts=prompts
    )


# MEMES

@app.route("/memes")
def memes():
    return render_template("memes.html")


if __name__ == "__main__":
    app.run(debug=True)