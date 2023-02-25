all: build up test
.PHONY: all

IMG=ad-lambda-mail
CONTAINER_NAME=lambda_mail

build:
	@echo "buildando imagem ${IMG}"
	@docker buildx build . -t "${IMG}"

up:
	@echo "subindo container"
	@docker run --name "${CONTAINER_NAME}" -d -p 9000:8080 "${IMG}"
	@sleep 1

test:
	@echo "testando lambda function"
	@curl -s -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}' | jq . 

clean:
	@echo "limpando o ambiente: container -> ${CONTAINER_NAME} e image -> ${IMG}"
	@docker container stop "${CONTAINER_NAME}"
	@docker container rm "${CONTAINER_NAME}"
	@docker image rm "${IMG}"
	@docker image prune -f

