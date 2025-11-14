from rest_framework import serializers
# Temporariamente desabilitamos a validação de senha do Django
# para permitir senhas simples em registros rápidos durante o desenvolvimento.
# Para reativar, descomente a importação e os validators abaixo.
# from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from .models import (
    Usuario,
    Professor,
    Coordenador,
    Empresa,
    Proposta,
    Projeto,
    Grupo,
    HallOfFame,
)


class RegisterSerializer(serializers.Serializer):
    """Serializer para registro que aceita papel (role) e cria o tipo correto.

    Campos aceitos: nome, email, password, password2, role (professor|coordenador|empresa), contato (opcional, para empresa).
    """
    ROLE_CHOICES = (
        ('professor', 'Professor'),
        ('coordenador', 'Coordenador'),
        ('empresa', 'Empresa'),
    )

    nome = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    # validators=[validate_password]  # desabilitado temporariamente
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    contato = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Os campos de senha não coincidem."})
        return attrs

    def create(self, validated_data):
        # Remover campo auxiliar
        validated_data.pop('password2', None)
        role = validated_data.pop('role')
        contato = validated_data.pop('contato', '')
        senha_raw = validated_data.pop('password')
        senha_hashed = make_password(senha_raw)

        nome = validated_data.get('nome')
        email = validated_data.get('email')

        if role == 'professor':
            user = Professor.objects.create(nome=nome, email=email, senha=senha_hashed)
            return user
        if role == 'coordenador':
            user = Coordenador.objects.create(nome=nome, email=email, senha=senha_hashed)
            return user
        # empresa
        user = Empresa.objects.create(nome=nome, email=email, senha=senha_hashed, contato=contato)
        return user

    def to_representation(self, instance):
        """Retorna uma representação simples do objeto criado.

        Evita que o DRF tente acessar campos como `role` diretamente no modelo
        (o que causava AttributeError quando o objeto era Empresa/Professor/Coordenador).
        """
        role = 'Usuário'
        contato = ''
        if isinstance(instance, Professor):
            role = 'Professor'
        elif isinstance(instance, Coordenador):
            role = 'Coordenador'
        elif isinstance(instance, Empresa):
            role = 'Empresa'
            contato = getattr(instance, 'contato', '')

        return {
            'id': instance.id,
            'nome': instance.nome,
            'email': instance.email,
            'role': role,
            'contato': contato,
        }


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Usuario"""
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'senha']
        extra_kwargs = {
            'senha': {'write_only': True}  # Senha não aparece em leituras
        }


class ProfessorSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Professor"""
    projetos_detalhes = serializers.SerializerMethodField()
    
    class Meta:
        model = Professor
        fields = ['id', 'nome', 'email', 'senha', 'projetos', 'projetos_detalhes']
        extra_kwargs = {
            'senha': {'write_only': True}
        }
    
    def get_projetos_detalhes(self, obj):
        """Retorna lista de títulos dos projetos"""
        return [projeto.titulo for projeto in obj.projetos.all()]


class CoordenadorSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Coordenador"""
    projetos_detalhes = serializers.SerializerMethodField()
    
    class Meta:
        model = Coordenador
        fields = ['id', 'nome', 'email', 'senha', 'projetos', 'projetos_detalhes']
        extra_kwargs = {
            'senha': {'write_only': True}
        }
    
    def get_projetos_detalhes(self, obj):
        """Retorna lista de títulos dos projetos"""
        return [projeto.titulo for projeto in obj.projetos.all()]


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Empresa"""
    total_projetos = serializers.SerializerMethodField()
    total_propostas = serializers.SerializerMethodField()
    
    class Meta:
        model = Empresa
        fields = [
            'id', 'nome', 'email', 'senha', 'contato',
            'projetos_associados', 'total_projetos', 'total_propostas'
        ]
        extra_kwargs = {
            'senha': {'write_only': True}
        }
    
    def get_total_projetos(self, obj):
        """Retorna o total de projetos associados"""
        return obj.projetos_associados.count()
    
    def get_total_propostas(self, obj):
        """Retorna o total de propostas enviadas"""
        return obj.propostas.count()


class PropostaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Proposta"""
    empresa_nome = serializers.CharField(source='empresa.nome', read_only=True)
    
    class Meta:
        model = Proposta
        fields = [
            'id', 'titulo', 'descricao', 'data_envio', 'status',
            'anexos', 'empresa', 'empresa_nome'
        ]
        read_only_fields = ['data_envio', 'status']
        # empresa é opcional no serializer (preenchido automaticamente se for empresa logada)
        extra_kwargs = {
            'empresa': {'required': False, 'allow_null': True}
        }


class ProjetoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Projeto"""
    professor_nome = serializers.CharField(source='professor_responsavel.nome', read_only=True)
    empresa_nome = serializers.CharField(source='empresa_associada.nome', read_only=True)
    coordenador_nome = serializers.CharField(source='aprovado_por.nome', read_only=True)
    proposta_titulo = serializers.CharField(source='proposta.titulo', read_only=True)
    
    class Meta:
        model = Projeto
        fields = [
            'id', 'titulo', 'descricao', 'status', 'progresso',
            'curso_turma', 'alunos', 'professor_responsavel', 'professor_nome',
            'empresa_associada', 'empresa_nome', 'aprovado_por', 'coordenador_nome',
            'proposta', 'proposta_titulo', 'data_inicio', 'data_final', 'anexos'
        ]


class GrupoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Grupo"""
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    total_projetos = serializers.SerializerMethodField()
    
    class Meta:
        model = Grupo
        fields = ['id', 'tipo', 'tipo_display', 'projetos', 'total_projetos']
    
    def get_total_projetos(self, obj):
        """Retorna o total de projetos no grupo"""
        return obj.projetos.count()


class HallOfFameSerializer(serializers.ModelSerializer):
    """Serializer para o modelo HallOfFame"""
    projeto_titulo = serializers.CharField(source='projeto.titulo', read_only=True)
    projeto_descricao = serializers.CharField(source='projeto.descricao', read_only=True)
    
    class Meta:
        model = HallOfFame
        fields = ['id', 'projeto', 'projeto_titulo', 'projeto_descricao', 'destaque']
