import os

from app.utils.LayoutEngine import LayoutEngine

base = os.path.dirname(__file__)
lE = LayoutEngine(base=base, module="about")

about_section = lE.build()
