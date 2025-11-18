
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class ButtonBlock(blocks.StructBlock):
    """
    A reusable block for creating call-to-action buttons.
    """
    button_text = blocks.CharBlock(required=True, help_text="The text to display on the button.")
    button_link = blocks.URLBlock(required=True, help_text="The URL the button should link to.")

    class Meta:
        template = "blocks/button_block.html"
        icon = "link"
        label = "Button"


class BaseBannerBlock(blocks.StructBlock):
    """
    An abstract base block for creating banner components.
    """
    background_image = ImageChooserBlock(required=True, help_text="The background image for the banner.")
    title = blocks.CharBlock(required=True, help_text="The main title for the banner.")
    subtitle = blocks.TextBlock(required=True, help_text="The subtitle or introductory text for the banner.")

    class Meta:
        abstract = True


class HeroBannerBlock(BaseBannerBlock):
    """
    A block for creating a prominent hero banner, typically at the top of a page.
    """
    button = ButtonBlock(required=False)
    overlay_opacity = blocks.FloatBlock(
        default=0.4,
        min_value=0,
        max_value=1,
        help_text="The opacity of the dark overlay on the background image (0.0 for transparent, 1.0 for fully opaque)."
    )

    class Meta:
        template = "blocks/hero_banner_block.html"
        icon = "placeholder"
        label = "Hero Banner"
        group = "Banners"


class CTABannerBlock(BaseBannerBlock):
    """
    A block for creating a call-to-action banner, encouraging users to take a specific action.
    """
    button = ButtonBlock(required=True)

    class Meta:
        template = "blocks/cta_banner_block.html"
        icon = "grip"
        label = "CTA Banner"
        group = "Banners"


class WelcomeMessageBlock(blocks.StructBlock):
    """
    A block for displaying a welcome message with an optional image.
    """
    title = blocks.CharBlock(required=True, help_text="The title of the welcome message.")
    message = blocks.RichTextBlock(required=True, help_text="The main content of the welcome message.")
    image = ImageChooserBlock(required=False, help_text="An optional image to display alongside the message.")

    class Meta:
        template = "blocks/welcome_message_block.html"
        icon = "edit"
        label = "Welcome Message"
        group = "Content"


class LinkBlock(blocks.StructBlock):
    """
    A block for representing a single link with an icon and label.
    """
    icon = blocks.CharBlock(default="link", help_text="The Font Awesome icon name (e.g., 'fa-link').")
    label = blocks.CharBlock(required=True, help_text="The text label for the link.")
    link = blocks.URLBlock(required=True, help_text="The URL for the link.")


class QuickLinksBlock(blocks.StructBlock):
    """
    A block for displaying a list of quick links.
    """
    links = blocks.ListBlock(LinkBlock())

    class Meta:
        template = "blocks/quick_links_block.html"
        icon = "link"
        label = "Quick Links"
        group = "Content"


class AnnouncementBlock(blocks.StructBlock):
    """
    A block for displaying a list of recent announcements or news articles.
    """
    title = blocks.CharBlock(required=True, help_text="The title for the announcements section.")
    post_limit = blocks.IntegerBlock(default=3, help_text="The maximum number of announcements to display.")

    class Meta:
        template = "blocks/announcement_block.html"
        icon = "megaphone"
        label = "Announcements"
        group = "Content"


class EventItemBlock(blocks.StructBlock):
    """
    A block for representing a single event.
    """
    event_title = blocks.CharBlock(required=True, help_text="The title of the event.")
    date = blocks.DateBlock(required=True, help_text="The date of the event.")
    description = blocks.TextBlock(required=True, help_text="A brief description of the event.")
    link = blocks.URLBlock(required=False, help_text="An optional link for more information about the event.")


class EventsBlock(blocks.StructBlock):
    """
    A block for displaying a list of upcoming events.
    """
    title = blocks.CharBlock(required=True, help_text="The title for the events section.")
    events = blocks.ListBlock(EventItemBlock())

    class Meta:
        template = "blocks/events_block.html"
        icon = "date"
        label = "Events"
        group = "Content"


class ValueItemBlock(blocks.StructBlock):
    """
    A block for representing a single Christian value.
    """
    icon = blocks.CharBlock(required=True, help_text="The Font Awesome icon name (e.g., 'fa-heart').")
    title = blocks.CharBlock(required=True, help_text="The title of the value.")
    description = blocks.TextBlock(required=True, help_text="A brief description of the value.")


class ChristianValuesBlock(blocks.StructBlock):
    """
    A block for displaying a set of Christian values.
    """
    values = blocks.ListBlock(ValueItemBlock())

    class Meta:
        template = "blocks/christian_values_block.html"
        icon = "heart"
        label = "Christian Values"
        group = "Content"


class HighlightItemBlock(blocks.StructBlock):
    """
    A block for representing a single academic highlight.
    """
    image = ImageChooserBlock(required=True, help_text="The image for the highlight.")
    title = blocks.CharBlock(required=True, help_text="The title of the highlight.")
    description = blocks.TextBlock(required=True, help_text="A brief description of the highlight.")


class AcademicHighlightsBlock(blocks.StructBlock):
    """
    A block for showcasing academic highlights.
    """
    items = blocks.ListBlock(HighlightItemBlock())

    class Meta:
        template = "blocks/academic_highlights_block.html"
        icon = "lightbulb"
        label = "Academic Highlights"
        group = "Content"


class TestimonialItemBlock(blocks.StructBlock):
    """
    A block for representing a single testimonial.
    """
    photo = ImageChooserBlock(required=True, help_text="The photo of the person giving the testimonial.")
    name = blocks.CharBlock(required=True, help_text="The name of the person.")
    role = blocks.CharBlock(required=True, help_text="The role or position of the person (e.g., 'Parent', 'Student').")
    quote = blocks.TextBlock(required=True, help_text="The testimonial quote.")


class TestimonialSliderBlock(blocks.StructBlock):
    """
    A block for displaying a slider of testimonials.
    """
    testimonials = blocks.ListBlock(TestimonialItemBlock())

    class Meta:
        template = "blocks/testimonial_slider_block.html"
        icon = "users"
        label = "Testimonial Slider"
        group = "Carousels and Sliders"


class GalleryPreviewBlock(blocks.StructBlock):
    """
    A block for displaying a preview of an image gallery.
    """
    images = blocks.ListBlock(ImageChooserBlock(), help_text="The images to display in the gallery preview.")
    columns = blocks.IntegerBlock(
        default=3,
        min_value=1,
        max_value=6,
        help_text="The number of columns to use for the gallery grid."
    )

    class Meta:
        template = "blocks/gallery_preview_block.html"
        icon = "image"
        label = "Gallery Preview"
        group = "Media"
