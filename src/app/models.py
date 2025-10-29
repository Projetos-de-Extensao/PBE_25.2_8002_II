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


class Diretor(models.Model):
	user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='diretor')

	def __str__(self):
		return f"Diretor: {self.user.nome}"


class Professor(models.Model):
	user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='professor')

	def __str__(self):
		return f"Professor: {self.user.nome}"


class Empresa(models.Model):
	nome = models.CharField(max_length=200)
	contato = models.CharField(max_length=200, blank=True)

	def __str__(self):
		return self.nome


class Coordenacao(models.Model):
	nome = models.CharField(max_length=200)
	email = models.EmailField(blank=True)

	def __str__(self):
		return self.nome


class Projeto(models.Model):
	titulo = models.CharField(max_length=250)
	descricao = models.TextField(blank=True)
	status = models.CharField(max_length=100, blank=True)
	progresso = models.CharField(max_length=100, blank=True)

	curso_turma = models.CharField(max_length=200, blank=True)
	alunos = models.TextField(blank=True)

	professor_responsavel = models.ForeignKey('Professor', null=True, blank=True, on_delete=models.SET_NULL, related_name='projetos')
	empresa_associada = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL, related_name='projetos')
	aprovado_por = models.ForeignKey(Coordenacao, null=True, blank=True, on_delete=models.SET_NULL, related_name='projetos_aprovados')

	data_inicio = models.DateField(null=True, blank=True)
	data_final = models.DateField(null=True, blank=True)

	etapa_atual = models.IntegerField(null=True, blank=True)
	etapa_final = models.IntegerField(null=True, blank=True)
	etapa_total = models.IntegerField(null=True, blank=True)

	anexos = models.TextField(blank=True, help_text='URLs ou descrições dos anexos')

	# projetos vinculados (relacionamento N..N com outros projetos)
	projetos_vinculados = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='projetos_vinculantes')

	def __str__(self):
		return self.titulo


class Grupo(models.Model):
	TIPO_CHOICES = (
		('I', 'Grupo I'),
		('II', 'Grupo II'),
	)
	tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
	projetos = models.ManyToManyField(Projeto, blank=True, related_name='grupos')

	def __str__(self):
		return f"Grupo {self.get_tipo_display()} ({self.id})"


class HallOfFame(models.Model):
	projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='hall_of_fame_entries')
	destaque = models.IntegerField(default=0, help_text='Posição ou prioridade do destaque')

	def __str__(self):
		return f"HallOfFame: {self.projeto.titulo} (#{self.destaque})"

