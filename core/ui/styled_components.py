from dash import dcc, html


def styled_input(id, placeholder="", type="text", size="md", **kwargs):
    size_class = {
        "sm": "na-input-sm",
        "md": "na-input-md",
        "lg": "na-input-lg",
    }.get(size, "na-input-md")

    return dcc.Input(
        id=id,
        placeholder=placeholder,
        type=type,
        className=f"na-input {size_class}",
        **kwargs,
    )


def styled_textarea(id, placeholder="", **kwargs):
    return dcc.Textarea(
        id=id,
        placeholder=placeholder,
        className="na-textarea",
        **kwargs,
    )


def styled_dropdown(id, options=None, placeholder="", **kwargs):
    return dcc.Dropdown(
        id=id,
        options=options or [],
        placeholder=placeholder,
        className="na-dropdown",
        **kwargs,
    )


def styled_radioitems(id, options=None, value=None, **kwargs):
    """
    RadioItems tipo botones redondeados.
    El CSS se encarga del estilo; aquí solo usamos className.
    """
    return dcc.RadioItems(
        id=id,
        options=options or [],
        value=value,
        className="na-radio-group",
        inputClassName="na-radio-item",
        labelClassName="na-radio-item-label",
        **kwargs,
    )


def styled_button(id, label, kind="primary", **kwargs):
    class_map = {
        "primary": "na-btn-primary",
    }
    return html.Button(
        label,
        id=id,
        className=class_map.get(kind, "na-btn-primary"),
        **kwargs,
    )


def input_with_tooltip(id, placeholder, tooltip_text, type="text", size="md", **kwargs):
    """
    Wrapper: input + tooltip que aparece al hacer hover sobre el input.
    """
    return html.Div(
        className="na-input-wrapper",
        children=[
            styled_input(
                id=id, placeholder=placeholder, type=type, size=size, **kwargs
            ),
            html.Div(tooltip_text, className="na-tooltip"),
        ],
    )
