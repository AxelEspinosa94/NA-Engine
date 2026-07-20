from dash import html, dcc

# Importar layouts de módulos
from .home_layout import home_layout
from .interpolation_layout import interpolation_section
from .integration_layout import integration_section
from .linear_algebra_layout import linear_algebra_section
from .numerical_derivative_layout import derivative_section
from .non_linear_layout import nonlinear_section
from .ode_layout import ode_section
from .docs_layout import docs_section

layout = html.Div(
    id="app-container",
    children=[

        # ============================
        # HEADER
        # ============================
        html.Header(
            id="app-header",
            children=[
                html.Div(id="logo-left", children=[html.Img(src="/assets/B-Izq.png", className="header-logo")]),
                html.Div(id="title-block", children=[html.H1("NA‑Engine"), html.H3("Numerical Analysis Engine")]),
                html.Div(id="logo-right", children=[html.Img(src="/assets/B-Der.png", className="header-logo")]),
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
                html.Button("Álgebra Lineal", id="tab-linear-algebra", className="nav-btn"),
                html.Button("Derivadas", id="tab-numerical-derivative", className="nav-btn"),
                html.Button("Ecuaciones No Lineales", id="tab-nonlinear", className="nav-btn"),
                html.Button("Ecuaciones Diferenciales", id="tab-odes", className="nav-btn"),
                html.Button("Documentación", id="tab-docs", className="nav-btn"),
                html.Button("Tema", id="toggle-theme", className="nav-btn"),
            ],
        ),

        # ============================
        # MAIN CONTENT
        # ============================
        html.Main(
            id="main-content",
            children=[
                html.Section(id="home-section", className="section active", children=[home_layout]),
                html.Section(id="section-interpolation", className="section", children=[interpolation_section]),
                html.Section(id="section-integration", className="section", children=[integration_section]),
                html.Section(id="section-linear-algebra", className="section", children=[linear_algebra_section]),
                html.Section(id="section-numerical-derivative", className="section", children=[derivative_section]),
                html.Section(id="section-nonlinear", className="section", children=[nonlinear_section]),
                html.Section(id="section-odes", className="section", children=[ode_section]),
                html.Section(id="section-docs", className="section", children=[docs_section]),
            ],
        ),
    ],
)
