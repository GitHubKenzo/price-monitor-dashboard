from app import render_content
from app import update_product_graph
from data_loader import load_price_history


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


def test_tab1_graph_exists():
    content = render_content("tab-1")
    collect_ids(content)
    # Graph は id を持たないが、dcc.Graph が存在することを確認
    assert any("Graph" in str(type(c)) for c in content.children)


def test_tab3_dropdown_and_graph_exist():
    content = render_content("tab-3")
    ids = collect_ids(content)
    assert "product-dropdown" in ids
    assert "product-graph" in ids


def test_update_product_graph_returns_figure():
    df = load_price_history()
    product = df["product_name"].iloc[0]
    fig = update_product_graph(product)
    assert "data" in fig
