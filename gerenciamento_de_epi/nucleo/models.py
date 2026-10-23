from django.db import models

# Create your models here.
class Colaboradores(models.Model):
    id_colaborador = models.AutoField
    setor = models.ForeignKey("nucleo.Setor", verbose_name='Setor', on_delete=models.CASCADE, null=False)
    nome = models.CharField(max_length=50, null=False, blank=False)
    status = models.BooleanField(default=True)
    cpf = models.CharField(max_length=11, null=False, blank=False)
    def __str__(self):
        return self.nome

class Setor(models.Model):
    nome = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.nome
    
class EPI_Categoria(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    Descricao=models.CharField(max_length=100, null=True, blank=True)

class EPI(models.Model):
    id_epi = models.AutoField
    categoria = models.ForeignKey("nucleo.EPI_Categoria", verbose_name='Categoria', on_delete=models.CASCADE)
    Nome = models.CharField(max_length=45, null=False, blank=False)
    Estoque=models.PositiveBigIntegerField(default=5)

#class emprestimo
#   

#class itens_emprestimo
# 
