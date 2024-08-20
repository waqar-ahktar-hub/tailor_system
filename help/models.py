from django.db import models

class HelpCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class HelpTopic(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(HelpCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    help_topic = models.ForeignKey(HelpTopic, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback for {self.help_topic.title}'
