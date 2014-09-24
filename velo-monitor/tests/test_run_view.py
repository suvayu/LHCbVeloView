from collections import OrderedDict
import unittest2 as unittest

import mock
from lxml.html import fromstring as parse_html

import velo_monitor
from velo_monitor.run_view import sanitise

# Run view pages dictionary fixture
RUN_VIEW_PAGES = OrderedDict([
    ('start_page', {
        'title': 'Start Page',
        'plots': [
            # This plot is implicitly *not* sensor dependent
            {
                'title': 'Plot one',
                'name': 'plot_one'
            }
        ]
    }),
    ('other_page', {
        'title': 'Other Page',
        'plots': [
            {
                'title': 'Sensor plot one',
                'name': 'sensor_plot_one_{0:03d}',
                'sensor_dependent': True
            },
            {
                'title': 'Sensor plot two',
                'short': 'Snsr plot 2',
                'name': 'sensor_plot_two_{0}',
                'sensor_dependent': True
            },
            {
                'title': 'General plot',
                'name': 'general_plot'
            }
        ]
    }),
    # This page has no plots, and that's OK
    ('extra_page', {
        'title': 'Extra page'
    })
])

# Default children dictionary fixture, setting a default run_view page
DEFAULT_CHILDREN = {
    'run_view': 'run_view/start_page'
}


@mock.patch('velo_monitor.run_view.pages', RUN_VIEW_PAGES)
class TestRunView(unittest.TestCase):
    def setUp(self):
        self.app = velo_monitor.create_app()
        self.app.config['TESTING'] = True
        self.app.config['DEFAULT_CHILDREN'] = DEFAULT_CHILDREN
        self.client = self.app.test_client()

    def get(self, path):
        """Return an pq instance of the lxml parsed document at path."""
        rv = self.client.get(path, follow_redirects=True)
        return parse_html(rv.data)

    def post(self, path, data):
        """Return an pq instance of the lxml parsed document at path."""
        rv = self.client.post(path, data=data, follow_redirects=True)
        return parse_html(rv.data)

    def test_sanitise_filter(self):
        """Filter lowercases and replaces non-alphanumeric characters with _."""
        s = "|P~2;-u)o.N4j]bwD^ql=vKK#'N9|Y]]hEAj:8;=9|Jj2[8=/'Y!"
        s_safe = "_P_2__u_o_N4j_bwD_ql_vKK__N9_Y__hEAj_8__9_Jj2_8___Y_".lower()
        self.assertEqual(sanitise(s), s_safe)

    def test_404_on_invalid_page(self):
        """Should show 404 page on page not in dictionary."""
        doc = self.get('/run_view/fake_page')
        header = doc.cssselect('#main > h1')[0].text_content()
        self.assertIn('404', header)
        self.assertIn('Page not found', header)

    def test_display_page(self):
        """Should display current page name as a header and pages in sidebar."""
        doc = self.get('/run_view/extra_page')
        header = doc.cssselect('#main > h1')[0].text_content()
        nav = doc.cssselect('.nav-sidebar li')
        self.assertEqual(len(nav), len(RUN_VIEW_PAGES.keys()))
        self.assertEqual(header, 'Extra page')

    def test_default_page(self):
        """Should display default page if none is specified."""
        doc = self.get('/run_view')
        header = doc.cssselect('#main > h1')[0].text_content()

        # Get the default page for the `run_view/` path and that page's title
        page_key = DEFAULT_CHILDREN['run_view'][len('run_view/'):]
        page_title = RUN_VIEW_PAGES[page_key]['title']

        self.assertNotIn('404', header)
        self.assertIn(page_title, header)

    def test_plot_per_tab(self):
        """Should display one tab per plot, each plot in its own tab pane.

        The short title should be display in the tab, if present, whilst the
        full title should be displayed in the pane header.
        """
        doc = self.get('/run_view/other_page')
        tabs = doc.cssselect('.run-view-tab')
        panes = doc.cssselect('.run-view-pane')
        plots = RUN_VIEW_PAGES['other_page']['plots']

        self.assertEqual(len(tabs), len(plots))
        self.assertEqual(len(panes), len(plots))
        for idx, (tab, pane) in enumerate(zip(tabs, panes)):
            title = plots[idx]['title']
            short = plots[idx].get('short', title)
            self.assertEqual(tab.text_content(), short)
            self.assertEqual(pane.cssselect('h1')[0].text_content(), title)

    def test_sensor_selector(self):
        """Sensor selector should be shown only when supported by a plot."""
        doc = self.get('/run_view/other_page')
        panes = doc.cssselect('.run-view-pane')
        plots = RUN_VIEW_PAGES['start_page']['plots']
        for idx, (pane, plot) in enumerate(zip(panes, plots)):
            selector = pane.cssselect('.sensor-selector:nth-child({0})'.format(idx))
            expected = int(plot.get('sensor_dependent', False))
            self.assertEqual(len(selector), expected)

    def test_default_sensor_number(self):
        """Sensor number should be set to zero if none is specified."""
        doc = self.get('/run_view/other_page')
        # We know the first plot is sensor dependent
        field = doc.cssselect('.run-view-pane:first-child .sensor-selector input')[0]
        self.assertEqual(field.value, '0')

    def test_invalid_sensor_numbers(self):
        """Invalid sensor numbers should be set to zero and an error shown."""
        doc = self.get('/run_view/other_page/999')
        field = doc.cssselect('.run-view-pane:first-child .sensor-selector input')[0]
        self.assertEqual(field.value, '0')

    def test_sensor_number_get(self):
        """Page should reflect the chosen sensor (GET request'ed)."""
        sensor = 32
        doc = self.get('/run_view/other_page/{0}'.format(sensor))
        # We know the first plot is sensor dependent
        field = doc.cssselect('.run-view-pane:first-child .sensor-selector input')[0]
        self.assertEqual(field.value, str(sensor))

    def test_sensor_number_post(self):
        """Page should reflect the chosen sensor (POST request'ed)."""
        sensor = 12
        doc = self.post('/run_view/other_page', {'sensor': sensor})
        field = doc.cssselect('.run-view-pane:first-child .sensor-selector input')[0]
        self.assertEqual(field.value, str(sensor))
