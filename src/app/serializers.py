from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
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


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de novos usuários"""
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Os campos de senha não coincidem."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data['senha'] = make_password(validated_data.pop('password'))
        user = Usuario.objects.create(**validated_data)
        return user


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
        read_only_fields = ['data_envio']


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
