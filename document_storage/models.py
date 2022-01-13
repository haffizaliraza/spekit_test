from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

STATE_TYPES = (
    (-1, _('Deleted')),
    (1, _('Active')),
)

class BaseModel(models.Model):
    created = models.DateTimeField(
        verbose_name=_('Creation date'),
        auto_now_add=True,
        editable=False,
    )
    modified = models.DateTimeField(
        verbose_name=_('Update date'),
        auto_now=True,
        editable=False,
    )
    state = models.SmallIntegerField(
        verbose_name=_('Publish state'),
        choices=STATE_TYPES,
        default=1,
    )

    class Meta:
        abstract = True


class Folder(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'


class DigitalDocuments(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True
    )
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="digital_documents_folder"
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'


class Topics(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True
    )
    folder = models.ForeignKey(
        Folder,
        related_name="topic_folder",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    document = models.ForeignKey(
        DigitalDocuments,
        related_name="topic_documents",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    short_form_descriptors = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    long_form_descriptors = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
