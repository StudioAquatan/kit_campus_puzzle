import uuid
import os
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.utils.safestring import mark_safe
from django.dispatch import receiver


def get_image_path(instance, filename):
    prefix = 'images/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


class Puzzle(models.Model):
    name = models.CharField('Puzzle Name', max_length=255)
    description = models.TextField('Description', default='')
    for_begginer = models.BooleanField('Beginner', default=True)
    bg_image = models.ImageField('BackGround', upload_to=get_image_path)
    is_test = models.BooleanField('Is Test', default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Parts(models.Model):
    name = models.CharField('Parts Name', max_length=255)
    x = models.FloatField('X', default=0.0)
    y = models.FloatField('Y', default=0.0)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.SET_NULL, related_name='parts', null=True, blank=True)
    img = models.ImageField('Image', upload_to=get_image_path)
    ratio = models.FloatField('Ratio', null=True, blank=True)
    most_far_distance = models.FloatField('Most far distance', default=0.0)

    class Meta:
        ordering = ['name']

    def bg_img_tag(self):
        return mark_safe('<img src="{}">'.format(self.puzzle.bg_image.url))

    def __str__(self):
        return self.name


@receiver(models.signals.pre_save, sender=Parts)
def register_ratio(sender, **kwargs):
    parts = kwargs.get('instance')
    parts.ratio = calculate_ratio(parts)
    parts.most_far_distance = calculate_most_far_distance(parts)


@receiver(models.signals.post_save, sender=Puzzle)
def reregister_ratio(sender, instance, **kwargs):
    for parts in instance.parts.all():
        parts.ratio = calculate_ratio(parts)
        parts.most_far_distance = calculate_most_far_distance(parts)
        parts.save()


def calculate_ratio(parts):
    w = parts.img.width
    bg_w = parts.puzzle.bg_image.width
    return Decimal(w / bg_w).quantize(Decimal('0.00001'), ROUND_HALF_UP) * 100


def calculate_most_far_distance(parts):
    init_coordinate = np.array([parts.x, parts.y])
    w, h = parts.img.width, parts.img.height
    bg_w, bg_h = parts.puzzle.bg_image.width, parts.puzzle.bg_image.height
    # 0 <= parts.x <= fixed_w
    fixed_w = (bg_w - w) / bg_w * 100
    # 0 <= parts.y <= fixed_h
    fixed_h = (bg_h - h) / bg_h * 100
    # 取り得る最も離れた点の座標
    corners = [[0, 0], [0, fixed_h], [fixed_w, 0], [fixed_w, fixed_h]]
    # 対象パーツの位置からユークリッド距離を算出
    distances = np.array([np.linalg.norm(init_coordinate - np.array(p)) for p in corners])
    # 降順に並び替えて最も大きな距離のものを返す
    return np.sort(distances)[::-1][0]
