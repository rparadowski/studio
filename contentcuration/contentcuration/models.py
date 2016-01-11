from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext as _


class Channel(models.Model):
    """ Permissions come from association with organizations """
    name = models.CharField(
        max_length= 100,
        verbose_name=_("channel name"),
    )
    description = models.TextField(
        max_length = 300,
        verbose_name=_("channel description"),
        help_text=_("Description of what a channel contains"),
    )
    author = models.CharField(
        max_length=100,
        verbose_name=_("channel author"),
        help_text=_("Channel author can be a person or an organization"),
    )
    editors = models.ManyToManyField(
        'auth.User',
        verbose_name=_("editors"),
        help_text=_("Users with edit rights"),
    )

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")


class TopicTree(models.Model):
    """Base model for all channels"""
    

    name = models.CharField(
        max_length=255,
        verbose_name=_("topic tree name"),
        help_text=_("Displayed to the user"),
    )
    channel = models.ForeignKey(
        'Channel',
        verbose_name=_("channel"),
        null=True,
        help_text=_("For different versions of the tree in the same channel (trash, edit, workspace)"),
    )
    root_node = models.ForeignKey(
        'Node',
        verbose_name=_("root node"),
        null=True,
        help_text=_(
            "The starting point for the tree, the title of it is the "
            "title shown in the menu"
        ),
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_("Published"),
        help_text=_("If published, students can access this channel"),
    )
    
    class Meta:
        verbose_name = _("Topic tree")
        verbose_name_plural = _("Topic trees")


class Node(MPTTModel):
    """
    By default, all nodes have a title and can be used as a topic.
    """

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("modified"))

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    title = models.CharField(
        max_length=50,
        verbose_name=_("title"),
        default=_("Title"),
        help_text=_("Node title"),
    )

    description = models.TextField(
        max_length=200,
        verbose_name=_("description"),
        default=_("Description"),
        help_text=_("Brief description of what is contained in this folder"),
    )

    published = models.BooleanField(
        default=False,
        verbose_name=_("Published"),
        help_text=_("If published, students can access this item"),
    )

    deleted = models.BooleanField(
        default=False,
        verbose_name=_("Deleted"),
        help_text=_(
            "Indicates that the node has been deleted, and should only "
            "be retrievable through the admin backend"
        ),
    )

    sort_order = models.FloatField(
        max_length=50,
        #unique=True,
        default=0,
        verbose_name=_("sort order"),
        help_text=_("Ascending, lowest number shown first"),
    )

    license_owner = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Organization of person who holds the essential rights"),
    )

    license = models.ForeignKey(
        'ContentLicense',
        null=True,
        verbose_name=_("license"),
        help_text=_("License under which the work is distributed"),
    )

    kind = models.CharField(
        max_length=50,
        verbose_name=_("kind"),
        help_text=_("Type of node (topic, video, exercise, etc.)"),
        default="Topic"
    )

    @property
    def has_draft(self):
        return self.draft_set.all().exists()
    
    @property
    def get_draft(self):
        """
        NB! By contract, only one draft should always exist per node, this is
        enforced by the OneToOneField relation.
        :raises: Draft.DoesNotExist and Draft.MultipleObjectsReturned
        """
        return Draft.objects.get(publish_in=self)
    
    class MPTTMeta:
        order_insertion_by = ['sort_order']

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        # Do not allow two nodes with the same name on the same level
        unique_together = ('parent', 'title')



class ContentLicense(models.Model):
    name = models.CharField(
        max_length=255,
        default=(""),
        verbose_name=_("name"),
        help_text=_("Name of license, e.g. 'Creative Commons Share-Alike 2.0'"),
    )
    exists = models.BooleanField(
        default=False,
        verbose_name=_("license exists"),
        help_text=_("Tells whether or not a content item is licensed to share"),
    )


# If we decide to subclass Content:
#
# class ContentVideo(Content):
#     """
#     Model for video data
#     """
#
#     video_file = models.FileField(
#         blank=True,
#         null=True,
#         upload_to='contents/video/thumbnails/',
#         verbose_name=_("video file"),
#         help_text=_("Upload video here"),
#     )
#
#     thumbnail = models.ImageField(
#         null=True,
#         upload_to='contents/video/thumbnails/',
#         help_text=_("Automatically created when new video is uploaded")
#     )
#
#
# class ContentPDF(Content):
#     """
#     Model for video data
#     """
#     pdf_file = models.FileField(
#         blank=True,
#         null=True,
#         upload_to='contents/video/thumbnails/',
#         verbose_name=_("video file"),
#         help_text=_("Upload video here"),
#     )
#
#
# class Exercise(Content):
#     """
#     Model for Exercise data
#     """


class Exercise(models.Model):

    title = models.CharField(
        max_length=50,
        verbose_name=_("title"),
        default=_("Title"),
        help_text=_("Title of the content item"),
    )

    description = models.TextField(
        max_length=200,
        verbose_name=_("description"),
        default=_("Description"),
        help_text=_("Brief description of what this content item is"),
    )


class AssessmentItem(models.Model):

    type = models.CharField(max_length=50, default="multiplechoice")
    question = models.TextField(blank=True)
    answers = models.TextField(default="[]")
    exercise = models.ForeignKey('Exercise', related_name="all_assessment_items")
