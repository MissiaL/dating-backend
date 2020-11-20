
import factory
from playhouse.shortcuts import model_to_dict



class PeeweeModelFactory(factory.Factory):
    """
    Based on PeeweeModelFactory from factory_boy-peewee,
    but _create doesn't calculate next pk,
    so it works only with pk's that unique by design (eg, UUIDs)
    """

    class Meta:
        abstract = True

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        model = target_class.create(**kwargs)
        return model

