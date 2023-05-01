from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Хэштеги к публикациям'

    def __str__(self):
        return self.name
    

class PetType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Вид животного'
        ordering = ['name']

    def __str__(self):
        return self.name
    

class PetBreed(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Порода животного'
        ordering = ['name']

    def __str__(self):
        return self.name


class MyPet(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='pets'
    )
    pet_type = models.ManyToManyField(PetType, null=False,
                                      related_name='types')
    pet_breed = models.ManyToManyField(PetBreed, null=False,
                                       related_name='breeds')
    image = models.ImageField(upload_to='image/',
                              null=True, blank=True)
    video = models.FileField(upload_to='video/', null=True, blank=True,
                             validators=[FileExtensionValidator(
        allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)
    likes = models.ManyToManyField(User,blank=True,
                                   related_name='likes')
    
    class Meta:
        verbose_name_plural = 'Публикации животных'

    def __str__(self):
        return self.text
    

class PetTag(models.Model):
    tag = models.ManyToManyField(Tag,
                                 related_name='tags')
    pet = models.ForeignKey(MyPet,
                            on_delete=models.CASCADE,
                            related_name='pets')
    
    def __str__(self):
        return f'{self.tag}, {self.pet}'
    

class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments')
    pet = models.ForeignKey(
        MyPet, on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    likes = models.ManyToManyField(User, blank=True,
                                   related_name='likes')

    class Meta:
        verbose_name_plural = 'Комментарии к публикациям'

    def __str__(self):
        return self.text
    

class OwnerFollow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписывающийся пользователь')
    owner_following = models.ForeignKey(User,
                                        on_delete=models.CASCADE,
                                        related_name='following',
                                        verbose_name='Пользователь на '
                                        'которого подписываются')
    
    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user','owner_following'],
            name='uq_user_owner_following')]
        
    def __str__(self):
        return f'{self.user}, {self.owner_following}'
    

class PetFollow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='pet_follower',
                             verbose_name='Подписчик животного')
    pet_following = models.ForeignKey(User,
                                      on_delete=models.CASCADE,
                                      related_name='pet_following',
                                      verbose_name='Животное на '
                                      'которое подписываются')
    
    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'pet_following'],
            name='uq_user_pet_following')]
        
    def __str__(self):
        return f'{self.user}, {self.pet_following}'
