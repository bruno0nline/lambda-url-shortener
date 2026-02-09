# URL Shortener - Lambda Serverless

Aplicação serverless simples que encurta URLs usando AWS Lambda, API Gateway e DynamoDB.

## 💰 Custos

**GRÁTIS** dentro do AWS Free Tier:
- Lambda: 1M requisições/mês grátis
- DynamoDB: 25GB armazenamento + 25 unidades de leitura/escrita grátis
- API Gateway: 1M chamadas/mês grátis (primeiros 12 meses)

URLs expiram automaticamente após 30 dias (TTL do DynamoDB).

## 🚀 Deploy

```bash
# 1. Criar pacote Lambda
cd lambda
zip -r ../lambda.zip index.py
cd ..

# 2. Deploy com Terraform
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

# Resposta: {"short_id": "a1b2c3", "expires_in_days": 30}
```

**Acessar URL encurtada:**
```bash
curl -L https://SEU-API-ENDPOINT/a1b2c3
# Redireciona para URL original
```

## 🧹 Limpar recursos

```bash
terraform destroy
```

## 🏷️ Tags

Todos os recursos são automaticamente tagueados com:
- Project: url-shortener
- Environment: dev
- ManagedBy: terraform
- Owner: bruno
