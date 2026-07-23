from dash import html, dcc


home_layout = html.Div(
    id="home-container",
    children=[

        # ============================
        # HERO SECTION
        # ============================
        html.Div(
            id="hero-section",
            children=[
                html.Div(
                    id="hero-text",
                    children=[
                        html.H1("NA‑Engine"),
                        html.H3("Numerical Analysis Engine"),
                        html.P(
                            "Una plataforma modular para resolver problemas de "
                            "Interpolación, Integración, Derivación, Sistemas Lineales "
                            "y Ecuaciones Diferenciales."
                        ),
                        html.Button(
                            "Comenzar",
                            id="home-start-btn",
                            className="primary-btn"
                        ),
                    ],
                ),
                html.Div(
                    id="hero-graphic",
                    children=[
                        html.Img(src="/assets/hero2.png", className="hero-img")
                    ],
                ),
            ],
        ),

        # ============================
        # MODULE GRID
        # ============================
        html.Div(
            id="module-grid",
            children=[
                html.Div(
                    className="module-card",
                    children=[
                        html.H3("Interpolación"),
                        html.P("Newton, Lagrange, Splines Cúbicos."),
                        html.Button("Ir al módulo", id="go-interpolation", className="secondary-btn"),
                    ],
                ),
                html.Div(
                    className="module-card",
                    children=[
                        html.H3("Integración"),
                        html.P("Simpson, Trapecio, Combinaciones."),
                        html.Button("Ir al módulo", id="go-integration", className="secondary-btn"),
                    ],
                ),
                html.Div(
                    className="module-card",
                    children=[
                        html.H3("Álgebra Lineal"),
                        html.P("Solución de sistemas de ecuaciones y Operaciones de Matrices"),
                        html.Button("Ir al módulo", id="go-linear-algebra", className="secondary-btn"),
                    ],
                ),
                html.Div(
                    className="module-card",
                    children=[
                        html.H3("Derivación Numérica"),
                        html.P("Diferencias finitas, derivación simbólica."),
                        html.Button("Ir al módulo", id="go-numerical-derivative", className="secondary-btn"),
                    ],
                ),
                html.Div(
                    className="module-card",
                    children=[
                        html.H3("Ecuaciones No Lineales"),
                        html.P("Bisección, Falsa Posición, Secante, Newton y Punto Fijo."),
                        html.Button("Ir al módulo", id="go-nonlinear", className="secondary-btn"),
                    ],
                ),
                html.Div(
                    className="module-card",
                    children=[
                        html.H3("Ecuaciones Diferenciales"),
                        html.P("Punto Fijo, Euler, Runge–Kutta."),
                        html.Button("Ir al módulo", id="go-odes", className="secondary-btn"),
                    ],
                ),
            ],
        ),

        # ============================
        # DOCUMENTATION SECTION
        # ============================
        html.Div(
            id="docs-section",
            children=[
                html.H2("Documentación"),
                html.P(
                    "Consulta la documentación oficial de NA‑Engine, ejemplos, "
                    "tutoriales y referencias matemáticas."
                ),
                html.Button("Abrir Documentación", id="open-docs", className="primary-btn"),
            ],
        ),

        # ============================
        # FOOTER
        # ============================
        html.Footer(
            id="footer",
            children=[
                html.P("Desarrollado por Carlos Axel Espinosa Ramírez"),
                html.P("NA‑Engine © 2026 — MIT License"),
                html.Button("About", id="go-about", className="primary-btn"),                
            ],
        ),
    ],
)
