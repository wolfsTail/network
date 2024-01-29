from django.db import models

from users.models import User


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts", verbose_name="Автор"
    )
    title = models.CharField(max_length=128, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Публикацию"
        verbose_name_plural = "Публикации"
    
    def __str__(self):
        return f"author: {self.author} -> post:{self.title}"
    


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", verbose_name="Автор"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост"
    )
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
    
    def __str__(self):
        return f"{self.author} comment {self.post} at {self.created_at}"


class Reaction(models.Model):
    class Values(models.TextChoices):
        SMILE = "smile", "🙂"
        THUMB_UP = "thumb_up", "👍"
        LAUGH = "laugh", "😂"
        SAD = "sad", "😢"
        HEART = "heart", "❤️"
        FEAR = "fear", "😨"
        ANGER = "anger", "😡"
        HATRED = "hatred", "🤬"
        HAPPINESS = "happiness", "😊"
    
    value = models.CharField(max_length=16, choices=Values.choices, verbose_name="Значение", null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reactions", verbose_name="Автор"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="reactions", verbose_name="Публикация"
    )

    class Meta:
        verbose_name = "Реакцию"
        verbose_name_plural = "Реакции"
        constraints = [
            models.UniqueConstraint(fields=["author", "post"], name="unique_reaction"),
        ]

    def __str__(self):
        return f"{self.author} react {self.post}"


