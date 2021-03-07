from django.db import models

from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey


class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(User, on_delete=models.CASCADE)
    um = models.IntegerField(blank=True,null=True)

    class Meta:
        abstract=True


class ClaseModelo2(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    # uc = models.ForeignKey(User, on_delete=models.CASCADE)
    # um = models.IntegerField(blank=True,null=True)
    uc = UserForeignKey(auto_user_add=True,related_name='+')
    um = UserForeignKey(auto_user=True,related_name='+')

    class Meta:
        abstract=True



class Idioma(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Idiomas"

    def __str__(self):
        return self.nombre


class Frase(models.Model):
    idioma = models.ForeignKey(Idioma,on_delete=models.CASCADE)
    autor = models.CharField(max_length=50,default="Anónimo")
    frase = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Frases"

    def __str__(self):
        return "{} - {}".format(self.autor,self.idioma)