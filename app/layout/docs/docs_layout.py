import os

from app.utils.LayoutEngine import LayoutEngine

base = os.path.dirname(__file__)

lE = LayoutEngine(base=base, module="docs")

docs_section = lE.build()