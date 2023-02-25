# ad-lambda-mail
Active Directory lambda function para mandar emails para conta de usuarios com senha expirada

# Configuracao
.env
```.env
AD_SERVER='ip do servidor active directory'
BASE_DN='DC=EXEMPLO,DC=LOCAL'
BIND_DN='administrator@exemplo.local'
AUTH_PASS='senha-do-administrator'
SMTP_ADDR='ip do servidor smtp'
HOST_NAME='nomedoservidor'
SMTP_USER='pingutester' # sasl username
SMTP_AUTH_PASS='123' # sasl user passwd
MAX_AGE=42 # idade maxima de senha
DAYS_RANGE=7 # usuarios com até um numero x dias para expirar a senha receberao email
```

# Docker image
### Constra a imagem
```console
docker build . -t ad-lambda-mail
```
### Suba o container
```console
docker run --name lambda_mail -d -p 9000:8080 ad-lambda-mail
```
# Testando
### Chama a lambda function do container rodando
```console
curl -s -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

# Makefile para facilitar a vida
### Roda build-up-test
```console
make
```
### Constroi a imagem
```console
make build
```
### Sobe container
```console
make up
```
### Testa a funcao lambda
```console
make test
```
### Remove container e a imagem
```console
make clean
```

# Testando codigo com ward
Crie um virtualenv e instale o requirements-dev.txt

dentro do diretorio tests existe um teste `test_ad_lambda_mail.py`
```console
pip install -r requirements-dev.txt
```
Para testar as funcoes [ward](https://github.com/darrenburns/ward)
```console
ward
```

# Como criar e mandar imagem da lambda function para aws ecr
refs: https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html

### Para pegar o seu aws_account_id
```console
aws sts get-caller-identity
```
### Faça o login 
```console
aws ecr get-login-password --region sua-region | docker login --username AWS --password-stdin https://aws_account_id.dkr.ecr.sua-region.amazonaws.com
```
### Crie o repositorio ecr
```console
aws ecr create-repository --repository-name lambda-repo --image-scanning-configuration  scanOnPush=True --region sua-region
```
### Taggeie a imagem com o nome correto
```console
docker tag ad-lambda-mail:latest aws_account_id.dkr.ecr.sua-region.amazonaws.com/lambda-repo
```
### Mande para o repositorio ecr
```console
docker push aws_account_id.dkr.ecr.sua-region.amazonaws.com/lambda-repo
```
