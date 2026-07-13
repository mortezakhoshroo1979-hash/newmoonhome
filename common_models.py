from __future__ import annotations

from django.db import models


class TimeStampedModel(models.Model):
    """مدل پایه برای افزودن زمان ایجاد و آخرین بروزرسانی."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        abstract = True
