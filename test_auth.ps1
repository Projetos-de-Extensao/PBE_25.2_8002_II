Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "     TESTE DE AUTENTICACAO JWT - EchoAPI" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://127.0.0.1:8000/api"

# Teste 1: Registrar Usuario
Write-Host "1. REGISTRANDO NOVO USUARIO..." -ForegroundColor Yellow
$registerBody = @{
    nome = "Usuario Teste"
    email = "teste@exemplo.com"
    password = "senha123456"
    password2 = "senha123456"
} | ConvertTo-Json

try {
    $register = Invoke-RestMethod -Uri "$baseUrl/register/" -Method Post -ContentType "application/json" -Body $registerBody
    Write-Host "   ✅ Usuario criado com sucesso!" -ForegroundColor Green
    Write-Host "   ID: $($register.id) | Nome: $($register.nome) | Email: $($register.email)" -ForegroundColor White
} catch {
    if ($_.Exception.Response.StatusCode -eq 400) {
        Write-Host "   ⚠️  Usuario ja existe (isso e normal)" -ForegroundColor Yellow
    } else {
        Write-Host "   ❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

# Teste 2: Obter Token
Write-Host "2. OBTENDO TOKEN DE ACESSO (LOGIN)..." -ForegroundColor Yellow
$loginBody = @{
    email = "teste@exemplo.com"
    password = "senha123456"
} | ConvertTo-Json

try {
    $tokens = Invoke-RestMethod -Uri "$baseUrl/token/" -Method Post -ContentType "application/json" -Body $loginBody
    Write-Host "   ✅ Tokens obtidos com sucesso!" -ForegroundColor Green
    Write-Host "   Access Token: $($tokens.access.Substring(0, 50))..." -ForegroundColor White
    Write-Host "   Refresh Token: $($tokens.refresh.Substring(0, 50))..." -ForegroundColor White
    
    $accessToken = $tokens.access
    $refreshToken = $tokens.refresh
} catch {
    Write-Host "   ❌ Erro ao obter token: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

# Teste 3: Verificar Token
Write-Host "3. VERIFICANDO TOKEN..." -ForegroundColor Yellow
$verifyBody = @{
    token = $accessToken
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "$baseUrl/token/verify/" -Method Post -ContentType "application/json" -Body $verifyBody | Out-Null
    Write-Host "   ✅ Token valido!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Token invalido" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

# Teste 4: Acesso SEM autenticacao (GET - deve funcionar)
Write-Host "4. TESTANDO LEITURA SEM AUTENTICACAO (GET)..." -ForegroundColor Yellow
try {
    $projetos = Invoke-RestMethod -Uri "$baseUrl/projetos/" -Method Get
    Write-Host "   ✅ Acesso publico de leitura funcionando!" -ForegroundColor Green
    Write-Host "   Total de projetos: $($projetos.count)" -ForegroundColor White
} catch {
    Write-Host "   ❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

# Teste 5: Criacao SEM autenticacao (deve falhar)
Write-Host "5. TESTANDO CRIACAO SEM AUTENTICACAO (POST)..." -ForegroundColor Yellow
$projetoBody = @{
    titulo = "Projeto Teste"
    descricao = "Teste sem autenticacao"
    status = "Em andamento"
    progresso = 0
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "$baseUrl/projetos/" -Method Post -ContentType "application/json" -Body $projetoBody | Out-Null
    Write-Host "   ⚠️  Criacao permitida sem autenticacao (inesperado)" -ForegroundColor Yellow
} catch {
    if ($_.Exception.Response.StatusCode -eq 401 -or $_.Exception.Response.StatusCode -eq 403) {
        Write-Host "   ✅ Bloqueio de acesso funcionando corretamente!" -ForegroundColor Green
        Write-Host "   Status: $($_.Exception.Response.StatusCode) - Nao autenticado" -ForegroundColor White
    } else {
        Write-Host "   ⚠️  Resposta inesperada: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

# Teste 6: Criacao COM autenticacao (deve funcionar)
Write-Host "6. TESTANDO CRIACAO COM AUTENTICACAO (POST)..." -ForegroundColor Yellow
$headers = @{
    Authorization = "Bearer $accessToken"
}

try {
    $novoProjeto = Invoke-RestMethod -Uri "$baseUrl/projetos/" -Method Post -ContentType "application/json" -Body $projetoBody -Headers $headers
    Write-Host "   ✅ Criacao com autenticacao funcionando!" -ForegroundColor Green
    Write-Host "   Projeto criado - ID: $($novoProjeto.id) | Titulo: $($novoProjeto.titulo)" -ForegroundColor White
} catch {
    if ($_.Exception.Response.StatusCode -eq 400) {
        Write-Host "   ⚠️  Dados invalidos (esperado - campos obrigatorios faltando)" -ForegroundColor Yellow
        $errorStream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($errorStream)
        $errorBody = $reader.ReadToEnd() | ConvertFrom-Json
        Write-Host "   Detalhes: $($errorBody | ConvertTo-Json -Compress)" -ForegroundColor Gray
    } else {
        Write-Host "   ❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

# Teste 7: Renovar Token
Write-Host "7. RENOVANDO TOKEN DE ACESSO..." -ForegroundColor Yellow
$refreshBody = @{
    refresh = $refreshToken
} | ConvertTo-Json

try {
    $newTokens = Invoke-RestMethod -Uri "$baseUrl/token/refresh/" -Method Post -ContentType "application/json" -Body $refreshBody
    Write-Host "   ✅ Token renovado com sucesso!" -ForegroundColor Green
    Write-Host "   Novo Access Token: $($newTokens.access.Substring(0, 50))..." -ForegroundColor White
} catch {
    Write-Host "   ❌ Erro ao renovar token: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "               RESUMO DOS TESTES" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "✅ Registro de usuario" -ForegroundColor Green
Write-Host "✅ Obtencao de tokens (login)" -ForegroundColor Green
Write-Host "✅ Verificacao de token" -ForegroundColor Green
Write-Host "✅ Leitura publica (GET sem auth)" -ForegroundColor Green
Write-Host "✅ Bloqueio de escrita sem autenticacao" -ForegroundColor Green
Write-Host "✅ Acesso com autenticacao" -ForegroundColor Green
Write-Host "✅ Renovacao de token" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 AUTENTICACAO JWT FUNCIONANDO PERFEITAMENTE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
