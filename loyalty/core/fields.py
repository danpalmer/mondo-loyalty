from django.db.models import OneToOneField as DjangoOneToOneField
from django.db.models.fields.related_descriptors import \
    ReverseOneToOneDescriptor


class AutoReverseOneToOneDescriptor(ReverseOneToOneDescriptor):
    """
    One to one field descriptor that creates the related object if it does not
    exist.
    """
    def __get__(self, instance, type=None):
        try:
            return super().__get__(instance, type)
        except self.related.related_model.DoesNotExist:
            kwargs = {
                self.related.field.name: instance,
            }
            rel_obj = self.related.related_model._default_manager.create(
                **kwargs
            )
            setattr(instance, self.cache_name, rel_obj)
            return rel_obj


class AutoOneToOneField(DjangoOneToOneField):
    related_accessor_class = AutoReverseOneToOneDescriptor


class OneToOneFieldDescriptor(ReverseOneToOneDescriptor):
    """
    One to one field descriptor that returns None instead of raising an
    exception when the related object does not exist.
    """
    def __get__(self, *args, **kwargs):
        try:
            return super().__get__(*args, **kwargs)
        except self.related.related_model.DoesNotExist:
            return None


class OneToOneField(DjangoOneToOneField):
    related_accessor_class = OneToOneFieldDescriptor
