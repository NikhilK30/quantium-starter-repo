import sys
import os

# allow Python to find data_visualizer.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_visualizer import app


def get_all_ids(component):
    """
    Recursively collect all component IDs from Dash layout
    """
    ids = []

    if hasattr(component, "id") and component.id:
        ids.append(component.id)

    if hasattr(component, "children"):
        children = component.children

        if isinstance(children, list):
            for child in children:
                ids.extend(get_all_ids(child))
        elif children:
            ids.extend(get_all_ids(children))

    return ids


def test_header_present():
    ids = get_all_ids(app.layout)
    assert "header" in ids


def test_visualisation_present():
    ids = get_all_ids(app.layout)
    assert "visualization" in ids


def test_region_picker_present():
    ids = get_all_ids(app.layout)
    assert "region-picker" in ids