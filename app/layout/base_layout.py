from dash import html, dcc

# Importar layouts de módulos
from .home_layout import home_layout
from .interpolation_layout import interpolation_section
from .integration_layout import integration_section
from .ode_layout import ode_section
# Más adelante:
# from .derivatives_layout import derivatives_section
# from .systems_layout import systems_section
# from .matrices_layout import matrices_section


layout = html.Div(
    id="app-container",
    children=[

        # ============================
        # HEADER
        # ============================
        html.Header(
            id="app-header",
            children=[
                html.Div(id="logo-left", children=[html.Img(src="/assets/puma3.png", className="header-logo")]),
                html.Div(id="title-block", children=[html.H1("NA‑Engine"), html.H3("Numerical Analysis Engine")]),
                html.Div(id="logo-right", children=[html.Img(src="/assets/puma4.png", className="header-logo")]),
            ],
        ),

        # ============================
        # NAVBAR
        # ============================
        html.Nav(
            id="navbar",
            children=[
                html.Button("Home", id="tab-home", className="nav-btn"),
                html.Button("Interpolación", id="tab-interpolation", className="nav-btn"),
                html.Button("Integración", id="tab-integration", className="nav-btn"),
                html.Button("Punto Fijo / ODEs", id="tab-odes", className="nav-btn"),
                html.Button("Tema", id="toggle-theme", className="nav-btn"),
            ],
        ),

        # ============================
        # MAIN CONTENT
        # ============================
        html.Main(
            id="main-content",
            children=[
                html.Section(id="home-container", className="section active", children=[home_layout]),
                html.Section(id="section-interpolation", className="section", children=[interpolation_section]),
                html.Section(id="section-integration", className="section", children=[integration_section]),
                html.Section(id="section-odes", className="section", children=[ode_section]),
            ],
        ),
    ],
)
