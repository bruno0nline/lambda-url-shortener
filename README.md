# URL Shortener - Lambda Serverless

Aplicação serverless que encurta URLs usando AWS Lambda, API Gateway e DynamoDB.

## 🎯 Para que serve

Esta aplicação demonstra um caso de uso real de AWS Lambda:
- **Encurta URLs longas** em IDs de 6 caracteres (ex: `c14be8`)
- **Redireciona automaticamente** quando alguém acessa o link curto
- **Expira URLs antigas** após 30 dias usando TTL do DynamoDB
- **Escalável e sem servidor** - você só paga pelo que usar

## 🏗️ Como foi criada

A infraestrutura foi provisionada com **Terraform** e inclui:

- **AWS Lambda** (Python 3.12) - Processa requisições de encurtamento e redirecionamento
- **API Gateway HTTP** - Expõe 2 endpoints públicos:
  - `POST /shorten` - Encurta uma URL
  - `GET /{short_id}` - Redireciona para URL original
- **DynamoDB** - Armazena mapeamento de IDs curtos para URLs originais
- **IAM Role** - Permissões para Lambda acessar DynamoDB e CloudWatch Logs

Todos os recursos são **automaticamente tagueados** com:
- `Project: url-shortener`
- `Environment: dev`
- `ManagedBy: terraform`
- `Owner: bruno`

## 💰 Custos

**GRÁTIS** dentro do AWS Free Tier:
- Lambda: 1M requisições/mês grátis
- DynamoDB: 25GB armazenamento + 25 unidades de leitura/escrita grátis
- API Gateway: 1M chamadas/mês grátis (primeiros 12 meses)

## 🚀 Deploy

```bash
# 1. Criar pacote Lambda
cd lambda
zip -r ../lambda.zip index.py
cd ..

# 2. Deploy com Terraform (usando perfil Master)
terraform init
terraform plan
terraform apply

# 3. Pegar URL da API
terraform output api_endpoint
```

## 📝 Como usar

**Encurtar URL:**
```bash
curl -X POST https://SEU-API-ENDPOINT/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://aws.amazon.com/lambda"}'

# Resposta: {"short_id": "c14be8", "expires_in_days": 30}
```

**Acessar URL encurtada:**
```bash
curl -L https://SEU-API-ENDPOINT/c14be8
# Redireciona para URL original
```

## 🗑️ Como destruir

Para remover **todos os recursos** da AWS e evitar custos:

```bash
terraform destroy
```

Confirme com `yes` quando solicitado. Isso irá deletar:
- Lambda Function
- API Gateway
- DynamoDB Table
- IAM Role e Policies
- CloudWatch Logs

**Importante:** Após destruir, os links encurtados param de funcionar imediatamente.
