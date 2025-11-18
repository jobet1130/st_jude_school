
from wagtail.test.utils import WagtailPageTests

from home.models import (
    HomePage, AnnouncementsIndexPage, AnnouncementPage, EventsIndexPage, EventPage
)


class ModelTests(WagtailPageTests):
    """Tests for the models in the home app."""

    def setUp(self):
        """Set up the test environment."""
        # Get the automatically created homepage
        self.home_page = HomePage.objects.first()
        # Log in a user with permissions to create pages
        self.login()

    def test_homepage_is_accessible(self):
        """Test that the homepage is accessible."""
        response = self.client.get(self.home_page.url)
        self.assertEqual(response.status_code, 200)

    def test_announcement_index_page_creation(self):
        """Test that an AnnouncementsIndexPage can be created as a child of the HomePage."""
        announcements_index_page = AnnouncementsIndexPage(
            title="Announcements",
            slug="announcements",
            intro="Latest news and announcements.",
        )
        self.home_page.add_child(instance=announcements_index_page)
        self.assertTrue(AnnouncementsIndexPage.objects.filter(slug="announcements").exists())

    def test_announcement_page_creation(self):
        """Test that an AnnouncementPage can be created."""
        announcements_index_page = AnnouncementsIndexPage(
            title="Announcements",
            slug="announcements",
        )
        self.home_page.add_child(instance=announcements_index_page)

        announcement_page = AnnouncementPage(
            title="New School Uniforms",
            slug="new-school-uniforms",
            date="2024-05-10",
            body="<p>New school uniforms are now available.</p>",
        )
        announcements_index_page.add_child(instance=announcement_page)
        self.assertTrue(AnnouncementPage.objects.filter(slug="new-school-uniforms").exists())

    def test_events_index_page_creation(self):
        """Test that an EventsIndexPage can be created."""
        events_index_page = EventsIndexPage(
            title="Events",
            slug="events",
            intro="Upcoming events.",
        )
        self.home_page.add_child(instance=events_index_page)
        self.assertTrue(EventsIndexPage.objects.filter(slug="events").exists())

    def test_event_page_creation(self):
        """Test that an EventPage can be created."""
        events_index_page = EventsIndexPage(
            title="Events",
            slug="events",
        )
        self.home_page.add_child(instance=events_index_page)

        event_page = EventPage(
            title="School Fete",
            slug="school-fete",
            start_date="2024-06-15",
            location="School Hall",
            body="<p>Join us for our annual school fete.</p>",
        )
        events_index_page.add_child(instance=event_page)
        self.assertTrue(EventPage.objects.filter(slug="school-fete").exists())
