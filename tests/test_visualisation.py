import pytest
import chromedriver_autoinstaller  # ensures the correct ChromeDriver is available
from dash.testing.composite import DashComposite

# We import the Dash app instance defined in visualisation.py
from visualisation import app

# Install a matching ChromeDriver for the local Chrome version
chromedriver_autoinstaller.install()


def test_header_present(dash_duo: DashComposite):
    dash_duo.start_server(app)
    header = dash_duo.wait_for_element('h1', timeout=10)
    assert 'Pink Morsel Sales Visualisation' in header.text


def test_visualisation_present(dash_duo: DashComposite):
    dash_duo.start_server(app)
    graph = dash_duo.wait_for_element('#sales-chart', timeout=10)
    assert graph.tag_name == 'div'


def test_region_picker_present(dash_duo: DashComposite):
    dash_duo.start_server(app)
    radio = dash_duo.wait_for_element('#region-radio', timeout=10)
    # Ensure expected options exist in the radio group
    labels = [el.text for el in dash_duo.find_elements('#region-radio label')]
    expected = {'All', 'North', 'East', 'South', 'West'}
    assert expected.issubset(set(labels))
