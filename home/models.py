from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index

from home import blocks as home_blocks

class HomePage(Page):
    """
    The HomePage model, which is the main landing page for the school's website.
    It uses a StreamField to allow for a flexible and modular content structure.
    """
    max_count = 1
    intro = models.CharField(max_length=250, blank=True, null=True, help_text="A brief introduction to the school.")

    body = StreamField([
        ('hero_banner', home_blocks.HeroBannerBlock(group="Banners")),
        ('welcome_message', home_blocks.WelcomeMessageBlock(group="Content")),
        ('quick_links', home_blocks.QuickLinksBlock(group="Content")),
        ('announcements', home_blocks.AnnouncementBlock(group="Content")),
        ('events', home_blocks.EventsBlock(group="Content")),
        ('christian_values', home_blocks.ChristianValuesBlock(group="Content")),
        ('academic_highlights', home_blocks.AcademicHighlightsBlock(group="Content")),
        ('testimonial_slider', home_blocks.TestimonialSliderBlock(group="Carousels and Sliders")),
        ('gallery_preview', home_blocks.GalleryPreviewBlock(group="Media")),
        ('cta_banner', home_blocks.CTABannerBlock(group="Banners")),
    ], use_json_field=True, null=True, blank=True, help_text="The main content of the page, composed of different content blocks.")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    # Allow creating Announcement and Event index pages under home page
    subpage_types = ['home.AnnouncementsIndexPage', 'home.EventsIndexPage']

    class Meta:
        verbose_name = "Home Page"


class AnnouncementsIndexPage(Page):
    """
    A page to list all announcements.
    """
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    # Allow creating Announcement pages under this page
    subpage_types = ['home.AnnouncementPage']
    # Allow this page to be created under home page
    parent_page_types = ['home.HomePage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Get all live announcement pages that are children of this page
        announcements = self.get_children().live().specific().order_by('-first_published_at')
        context['announcements'] = announcements
        return context

    class Meta:
        verbose_name = "Announcements Index Page"


class AnnouncementPage(Page):
    """
    A page for a single announcement.
    """
    date = models.DateField("Post date")
    body = RichTextField()

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body'),
    ]

    # No subpages allowed
    subpage_types = []
    # Allow this page to be created under announcements index page
    parent_page_types = ['home.AnnouncementsIndexPage']

    class Meta:
        verbose_name = "Announcement Page"


class EventsIndexPage(Page):
    """
    A page to list all events.
    """
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    # Allow creating Event pages under this page
    subpage_types = ['home.EventPage']
    # Allow this page to be created under home page
    parent_page_types = ['home.HomePage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Get all live event pages that are children of this page
        events = self.get_children().live().specific().order_by('eventpage__start_date')
        context['events'] = events
        return context

    class Meta:
        verbose_name = "Events Index Page"


class EventPage(Page):
    """
    A page for a single event.
    """
    start_date = models.DateField("Start date")
    end_date = models.DateField("End date", null=True, blank=True, help_text="Leave blank for single-day events.")
    start_time = models.TimeField("Start time", null=True, blank=True)
    end_time = models.TimeField("End time", null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    body = RichTextField()

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('location'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('start_date'),
            FieldPanel('end_date'),
        ], heading="Event Dates"),
        MultiFieldPanel([
            FieldPanel('start_time'),
            FieldPanel('end_time'),
        ], heading="Event Times"),
        FieldPanel('location'),
        FieldPanel('body'),
    ]

    # No subpages allowed
    subpage_types = []
    # Allow this page to be created under events index page
    parent_page_types = ['home.EventsIndexPage']

    class Meta:
        verbose_name = "Event Page"
