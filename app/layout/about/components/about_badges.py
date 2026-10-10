from dash import html


def build_badges(badges):
    return html.Div(
        className="about-badges",
        children=[
            html.Img(
                src=(
                    f"https://img.shields.io/badge/{badge['label']}-{badge['color']}"
                    f"?logo={badge['logo']}&logoColor=white"
                ),
                className="about-badge",
            )
            for badge in badges
        ],
    )
