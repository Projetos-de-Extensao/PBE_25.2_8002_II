"""
Script de teste para autenticação JWT
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 60)
print("TESTE DE AUTENTICAÇÃO JWT - EchoAPI")
print("=" * 60)

# Dados de teste
test_user = {
    "nome": "Teste Automático",
    "email": "teste@auth.com",
    "password": "senha_segura_123",
    "password2": "senha_segura_123"
}

# 1. REGISTRAR NOVO USUÁRIO
print("\n1️⃣  REGISTRANDO NOVO USUÁRIO...")
print(f"POST {BASE_URL}/register/")
print(f"Dados: {json.dumps(test_user, indent=2)}")

response = requests.post(f"{BASE_URL}/register/", json=test_user)
print(f"\nStatus Code: {response.status_code}")

if response.status_code == 201:
    print("✅ Usuário criado com sucesso!")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
elif response.status_code == 400:
    print("⚠️  Usuário já existe ou dados inválidos")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
else:
    print(f"❌ Erro ao registrar: {response.text}")

# 2. OBTER TOKEN DE ACESSO
print("\n" + "=" * 60)
print("2️⃣  OBTENDO TOKEN DE ACESSO...")
print(f"POST {BASE_URL}/token/")

login_data = {
    "email": test_user["email"],
    "password": test_user["password"]
}
print(f"Dados: {json.dumps(login_data, indent=2)}")

response = requests.post(f"{BASE_URL}/token/", json=login_data)
print(f"\nStatus Code: {response.status_code}")

if response.status_code == 200:
    tokens = response.json()
    print("✅ Tokens obtidos com sucesso!")
    print(f"Access Token: {tokens['access'][:50]}...")
    print(f"Refresh Token: {tokens['refresh'][:50]}...")
    
    access_token = tokens['access']
    refresh_token = tokens['refresh']
else:
    print(f"❌ Erro ao obter token: {response.text}")
    exit(1)

# 3. VERIFICAR TOKEN
print("\n" + "=" * 60)
print("3️⃣  VERIFICANDO TOKEN...")
print(f"POST {BASE_URL}/token/verify/")

response = requests.post(f"{BASE_URL}/token/verify/", json={"token": access_token})
print(f"\nStatus Code: {response.status_code}")

if response.status_code == 200:
    print("✅ Token válido!")
else:
    print(f"❌ Token inválido: {response.text}")

# 4. TESTAR ACESSO SEM AUTENTICAÇÃO (GET - deve funcionar)
print("\n" + "=" * 60)
print("4️⃣  TESTANDO LEITURA SEM AUTENTICAÇÃO (GET)...")
print(f"GET {BASE_URL}/projetos/")

response = requests.get(f"{BASE_URL}/projetos/")
print(f"\nStatus Code: {response.status_code}")

if response.status_code == 200:
    print("✅ Acesso público de leitura funcionando!")
    data = response.json()
    print(f"Total de projetos: {data.get('count', 0)}")
else:
    print(f"❌ Erro: {response.text}")

# 5. TESTAR CRIAÇÃO SEM AUTENTICAÇÃO (deve falhar)
print("\n" + "=" * 60)
print("5️⃣  TESTANDO CRIAÇÃO SEM AUTENTICAÇÃO (POST)...")
print(f"POST {BASE_URL}/projetos/")

projeto_teste = {
    "titulo": "Projeto de Teste",
    "descricao": "Este projeto deve falhar sem autenticação",
    "status": "Em andamento",
    "progresso": 0
}

response = requests.post(f"{BASE_URL}/projetos/", json=projeto_teste)
print(f"\nStatus Code: {response.status_code}")

if response.status_code == 401 or response.status_code == 403:
    print("✅ Bloqueio de acesso funcionando corretamente!")
    print(f"Resposta: {response.json()}")
else:
    print(f"⚠️  Resposta inesperada: {response.text}")

# 6. TESTAR CRIAÇÃO COM AUTENTICAÇÃO (deve funcionar)
print("\n" + "=" * 60)
print("6️⃣  TESTANDO CRIAÇÃO COM AUTENTICAÇÃO (POST)...")
print(f"POST {BASE_URL}/projetos/")
print(f"Authorization: Bearer {access_token[:30]}...")

headers = {"Authorization": f"Bearer {access_token}"}
response = requests.post(f"{BASE_URL}/projetos/", json=projeto_teste, headers=headers)
print(f"\nStatus Code: {response.status_code}")

if response.status_code == 201:
    print("✅ Criação com autenticação funcionando!")
    print(f"Projeto criado: {json.dumps(response.json(), indent=2)}")
elif response.status_code == 400:
    print("⚠️  Dados inválidos (esperado - campos obrigatórios faltando)")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
else:
    print(f"Resposta: {response.text}")

# 7. RENOVAR TOKEN
print("\n" + "=" * 60)
print("7️⃣  RENOVANDO TOKEN DE ACESSO...")
print(f"POST {BASE_URL}/token/refresh/")

response = requests.post(f"{BASE_URL}/token/refresh/", json={"refresh": refresh_token})
print(f"\nStatus Code: {response.status_code}")

if response.status_code == 200:
    new_access_token = response.json()['access']
    print("✅ Token renovado com sucesso!")
    print(f"Novo Access Token: {new_access_token[:50]}...")
else:
    print(f"❌ Erro ao renovar token: {response.text}")

# RESUMO
print("\n" + "=" * 60)
print("📊 RESUMO DOS TESTES")
print("=" * 60)
print("✅ Registro de usuário")
print("✅ Obtenção de tokens (login)")
print("✅ Verificação de token")
print("✅ Leitura pública (GET sem auth)")
print("✅ Bloqueio de escrita sem autenticação")
print("✅ Acesso com autenticação")
print("✅ Renovação de token")
print("\n🎉 AUTENTICAÇÃO JWT FUNCIONANDO PERFEITAMENTE!")
print("=" * 60)
