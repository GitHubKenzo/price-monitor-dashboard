from app import app


def collect_ids(component):
    ids = []
    if hasattr(component, "id") and component.id is not None:
        ids.append(component.id)

    if hasattr(component, "children") and component.children is not None:
        children = component.children
        if not isinstance(children, (list, tuple)):
            children = [children]
        for child in children:
            ids.extend(collect_ids(child))
    return ids


def test_app_layout_exists():
    assert app.layout is not None


def test_static_ids_exist():
    ids = collect_ids(app.layout)
    assert "tabs" in ids
    assert "tab-content" in ids
