from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


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

class Emprestimo(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.PROTECT)
    data_emprestimo = models.DateField(default=timezone.localdate)
    observacao = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Empréstimo {self.pk} - {self.colaborador}"


class ItemEmprestimo(models.Model):
    class Condicao(models.TextChoices):
        BOA = "boa", "Boa condição"
        DANIFICADO = "danificado", "Danificado"
        PERDIDO = "perdido", "Perdido"

    emprestimo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE, related_name="itens")
    epi = models.ForeignKey(EPI, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    data_devolucao = models.DateField(null=True, blank=True)
    condicao_devolucao = models.CharField(max_length=12, choices=Condicao.choices, blank=True)

    def __str__(self):
        return f"{self.epi} x{self.quantidade}"