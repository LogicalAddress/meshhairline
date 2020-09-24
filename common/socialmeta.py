from wagtailmetadata.models import MetadataMixin


class FakeImage():
    def __init__(self, url):
        self.url = url
    def get_rendition(self, filter):
        return self

class CollectionMixin(MetadataMixin, object):

    def get_meta_title(self):
        """The title of this object"""
        return self.title

    def get_meta_url(self):
        """The URL of this object, including protocol and domain"""
        return self.get_full_url()

    def get_meta_description(self):
        """
        A short text description of this object.
        This should be plain text, not HTML.
        """
        return self.title

    def get_meta_image(self):
        """A relevant Wagtail Image to show. Optional."""
        return self.icon