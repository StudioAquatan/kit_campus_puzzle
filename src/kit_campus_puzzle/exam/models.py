import os
import uuid
import json
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth import models as auth_models
from django.dispatch import receiver
from PIL import Image
from puzzle.models import Puzzle


def get_image_path(instance, filename):
    prefix = 'result/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


class Rank(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name='rank')
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, related_name='rank')
    score = models.FloatField('Score', default=0.0)
    coordinates = models.TextField('Coordinates', default='')
    taken_at = models.DateTimeField('Taken At', auto_now_add=True)
    result_image = models.ImageField('Result Image', upload_to=get_image_path, blank=True, null=True)

    class Meta:
        ordering = ['score']

    def __str__(self):
        return '{} - {}'.format(self.puzzle.name, self.user.username)

    def calculate_score(self, answer: list):
        # POSTされた値から各パーツの座標を算出
        answer = [np.array([ans[0], ans[1]]) for ans in answer]
        # most_far_distance: 理論上最も遠くに配置された場合の座標と正解座標との距離
        # 上記の値と正解の座標をタプルにする
        coordinates = [(np.array([p.x, p.y]), p.most_far_distance) for p in self.puzzle.parts.all()]
        # 正解の座標と回答された座標との距離を求め、最も遠い距離との比を算出
        scores = [np.linalg.norm(ans - correct[0]) / correct[1] for ans, correct in zip(answer, coordinates)]
        # 平均を求め、スコアを算出
        score = 1 - np.average(scores)
        # %から変換しているので希に誤差が生じる。ここで値を丸める
        if score < 0:
            score = 0
        elif score > 1:
            score = 1
        return round(score * 100, 1)


@receiver(models.signals.pre_save, sender=Rank)
def create_image(sender, instance, **kwargs):
    coordinates = json.loads(instance.coordinates)
    bg = instance.puzzle.bg_image
    # %で格納されている値をpixelに変換する
    fixed_coordinates = [(int(point[0] * bg.width / 100.0), int(point[1] * bg.height / 100.0)) for point in coordinates]
    # 背景画像をコピー
    bg_copy = Image.open(bg.file.open()).copy()
    # パーツを上から重ねていく
    for parts, coordinate in zip(instance.puzzle.parts.all(), fixed_coordinates):
        p = Image.open(parts.img.file.open())
        bg_copy.paste(p, coordinate, p)
    # 一時的にバッファへ格納
    buffer = BytesIO()
    bg_copy.convert('RGB').save(fp=buffer, format='JPEG', quality=95)
    merged = ContentFile(buffer.getvalue())
    # メモリ上から直接保存
    instance.result_image = InMemoryUploadedFile(
        merged, None, str(instance.pk) + '.jpg', 'image/jpeg', merged.size, None
    )
