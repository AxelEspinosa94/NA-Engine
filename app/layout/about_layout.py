from dash import html

about_section = html.Div(
    id="about-container",
    children=[

        # Header
        html.Div(
            className="module-header",
            children=[
                html.H2("Acerca de NA‑Engine"),
                html.P("Información general del proyecto, versión, créditos y notas de desarrollo."),
            ],
        ),

        # Card: Version
        html.Div(className="card", children=[
            html.H3("Versión"),
            html.P(
                """
                NA‑Engine utiliza versionado semántico (SemVer). 
                La versión actual corresponde al último tag registrado en el repositorio.
                """
            ),
            html.Div(
                id="about-version-display",
                className="about-info-box",
                children=[
                    html.P("Versión instalada: v0.1.2")  # Puedes actualizarlo manualmente o por callback
                ],
            ),
        ]),

        # Card: Changelog
        html.Div(className="card", children=[
            html.H3("Changelog"),
            html.P("Resumen de los cambios más recientes en el proyecto."),
            html.Div(
                className="about-info-box",
                children=[
                    html.Ul([
                        html.Li("v0.1.2 — Added VERSIONING.md and release automation."),
                        html.Li("v0.1.0 — Added documentation module and theory renderer."),
                        html.Li("v0.0.x — Core architecture, UI, numerical modules."),
                    ])
                ],
            ),
        ]),

        # Card: Credits
        html.Div(className="card", children=[
            html.H3("Créditos"),
            html.P("Autoría y agradecimientos."),
            html.Div(
                className="about-info-box",
                children=[
                    html.P("Desarrollado por Axel Espinosa, M. Sc."),
                    html.P("Licencia: MIT"),
                ],
            ),
        ]),

        # Card: Documentation
        html.Div(className="card", children=[
            html.H3("Documentación"),
            html.P(
                """
                NA‑Engine incluye documentación teórica integrada directamente en la aplicación.
                Puedes consultarla desde la sección “Documentación Teórica”.
                """
            ),
        ]),

        # Card: Project Notes
        html.Div(className="card", children=[
            html.H3("Notas del Proyecto"),
            html.P(
                """
                NA‑Engine es una herramienta modular y extensible para análisis numérico,
                construida con Python 3.12 y Dash. Su arquitectura separa UI, validación,
                ejecución y renderizado para garantizar mantenibilidad y escalabilidad.
                """
            ),
        ]),
    ],
)
