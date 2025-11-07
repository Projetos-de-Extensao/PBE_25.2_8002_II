from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.nome} <{self.email}>"


class Professor(Usuario):  # <- Herda de Usuario
    projetos = models.ManyToManyField('Projeto', blank=True, related_name='professores')

    def __str__(self):
        return f"Professor: {self.nome}"


class Coordenador(Usuario):  # <- Também herda de Usuario
    projetos = models.ManyToManyField('Projeto', blank=True, related_name='coordenadores')

    def __str__(self):
        return f"Coordenador: {self.nome}"
# ==========================
# EMPRESA
# ==========================
class Empresa(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    contato = models.CharField(max_length=200, blank=True)
    projetos_associados = models.ManyToManyField('Projeto', blank=True, related_name='empresas')

    def __str__(self):
        return self.nome


# ==========================
# PROPOSTA
# ==========================
class Proposta(models.Model):
    titulo = models.CharField(max_length=250)
    descricao = models.TextField(blank=True)
    data_envio = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Em análise')
    anexos = models.TextField(blank=True, help_text='URLs ou descrições dos anexos da proposta')

    empresa = models.ForeignKey(
        'Empresa',
        on_delete=models.CASCADE,
        related_name='propostas',
        help_text='Empresa que enviou a proposta'
    )

    def __str__(self):
        return f"Proposta: {self.titulo} ({self.empresa.nome})"

# ==========================
# PROJETO
# ==========================
class Projeto(models.Model):
    titulo = models.CharField(max_length=250)
    descricao = models.TextField(blank=True)
    status = models.CharField(max_length=100, blank=True)
    progresso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Progresso em %')

    curso_turma = models.CharField(max_length=200, blank=True)
    alunos = models.TextField(blank=True, help_text='Lista de alunos participantes')

    professor_responsavel = models.ForeignKey(
        'Professor', null=True, blank=True, on_delete=models.SET_NULL, related_name='projetos_responsaveis'
    )
    empresa_associada = models.ForeignKey(
        'Empresa', null=True, blank=True, on_delete=models.SET_NULL, related_name='projetos_empresa'
    )
    aprovado_por = models.ForeignKey(
        'Coordenador', null=True, blank=True, on_delete=models.SET_NULL, related_name='projetos_aprovados'
    )

    proposta = models.OneToOneField(
        'Proposta', on_delete=models.CASCADE, related_name='projeto', null=False, blank=False
    )

    data_inicio = models.DateField(null=True, blank=True)
    data_final = models.DateField(null=True, blank=True)

    anexos = models.TextField(blank=True, help_text='URLs ou descrições dos anexos')

    def __str__(self):
        return self.titulo


# ==========================
# GRUPO
# ==========================
class Grupo(models.Model):
    TIPO_CHOICES = (
        ('I', 'Grupo I'),
        ('II', 'Grupo II'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    projetos = models.ManyToManyField(Projeto, blank=True, related_name='grupos')

    def __str__(self):
        return f"Grupo {self.get_tipo_display()} ({self.id})"


# ==========================
# HALL OF FAME
# ==========================
class HallOfFame(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='hall_of_fame_entries')
    destaque = models.IntegerField(default=0, help_text='Posição ou prioridade do destaque')

    def __str__(self):
        return f"HallOfFame: {self.projeto.titulo} (#{self.destaque})"
