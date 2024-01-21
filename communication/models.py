from django.db import models
from django.db.models import F, functions

from users.models import User


class Chat(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_1")
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_2")

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"
        constraints = [
            models.UniqueConstraint(
                functions.Greatest(F("user_1"), F("user_2")),
                functions.Least(F("user_1"), F("user_2")),
                name="unique_chat",
            )
        ]
    
    def __str__(self):
        return f"Chat from {self.user_1} to {self.user_2}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Message from {self.author} in {self.chat} at {self.created_at}"
