from dash import Input, Output

def register_navigation_callbacks(app):

    # Secciones en el mismo orden que los Outputs
    section_ids = [
        "home-container",
        "section-interpolation",
        "section-integration",
        "section-odes",
    ]

    # Todos los botones que pueden activar navegación
    button_ids = [
        # Navbar
        "tab-home",
        "tab-interpolation",
        "tab-integration",
        "tab-odes",

        # Home Dashboard
        "home-start-btn",
        "go-interpolation",
        "go-integration",
        "go-odes",
    ]

    # Mapeo dinámico: botón → índice de sección
    button_to_section = {
        # Navbar
        "tab-home": 0,
        "tab-interpolation": 1,
        "tab-integration": 2,
        "tab-odes": 3,

        # Home Dashboard
        "home-start-btn": 1,   # Comenzar → Interpolación
        "go-interpolation": 1,
        "go-integration": 2,
        "go-odes": 3,
    }

    @app.callback(
        [Output(sec, "className") for sec in section_ids],
        [Input(btn, "n_clicks_timestamp") for btn in button_ids],
    )
    def navigate(*timestamps):

        # Normalizar None → 0
        timestamps = [ts or 0 for ts in timestamps]

        # Determinar cuál botón fue presionado más recientemente
        last_clicked_index = timestamps.index(max(timestamps))

        # Obtener el ID del botón activado
        last_button_id = button_ids[last_clicked_index]

        # Determinar qué sección activar
        target_section = button_to_section.get(last_button_id, 0)

        # Construir dinámicamente las clases
        classes = [
            "section active" if i == target_section else "section"
            for i in range(len(section_ids))
        ]

        return classes
