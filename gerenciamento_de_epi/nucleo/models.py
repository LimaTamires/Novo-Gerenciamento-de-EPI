from django.db import models


class Setor(models.Model):
    nome = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Setores"

    def __str__(self):
        return self.nome


class Colaborador(models.Model):
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class EPICategoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categorias de EPI"

    def __str__(self):
        return self.nome


class EPI(models.Model):
    categoria = models.ForeignKey(EPICategoria, on_delete=models.PROTECT)
    nome = models.CharField(max_length=45)
    estoque = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.nome