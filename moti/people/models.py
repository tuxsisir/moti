from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """
    extended user model
    """

    name = models.CharField(max_length=255, blank=True)
    age = models.CharField(max_length=255, blank=True)

    relations = models.ManyToManyField(
        "self",
        related_name="relationships",
        symmetrical=False,
        through="UserRelation",
        blank=True,
    )

    def __str__(self):
        return f"User: <{self.username}>"


class UserRelation(models.Model):
    RELATION_TYPES = (
        ("GRANDPARENT", "GRANDPARENT"),
        ("PARENT", "PARENT"),
        ("PARTNER", "PARTNER"),
        ("CHILD", "CHILD"),
        ("FRIEND", "FRIEND"),
    )

    source = models.ForeignKey(
        to=User, related_name="as_a_source", on_delete=models.CASCADE
    )  # such as source is parent
    target = models.ForeignKey(
        to=User, related_name="as_a_target", on_delete=models.CASCADE
    )  # such as target is child
    relation_type = models.CharField(choices=RELATION_TYPES, blank=True, max_length=12)

    def __str__(self):
        return f"{self.target} is {self.relation_type} of {self.source}"

    class Meta:
        unique_together = ('source', 'target', 'relation_type',) # avoid duplicate relations
