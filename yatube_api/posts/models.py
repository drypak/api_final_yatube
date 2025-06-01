from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """
    Группа постов.

    title - название группы,
    slug - уникальный идентификатор в URL,
    description - описание группы.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    Модель поста.

    text - текст поста,
    pub_date - дата публикации,
    author - автор(юзер),
    image - картинка(опционально),
    group - группа(опционально).
    """

    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Комментарий к посту.

    author - кто написал,
    post - к какому посту,
    text - текст комментария,
    created - дата добавления.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    """
    Модель подписки.

    user - кто подписывается,
    following - на кого подписываются.

    Подписка уникальна (user + following).
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follows',
        null=True
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        null=True
    )

    class Meta:
        unique_together = ('user', 'following')

    def __str__(self):
        return f'{self.user} follows {self.following}'
