deploy-all: rabbitmq redis deploy-app deploy-consumer

kind-cluster:
	kind create cluster --config kind-cluster.yaml --image=kindest/node:v1.21.2

rabbitmq:
	kubectl apply -f "https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml"
	kubectl apply -f rabbitmq-cluster.yaml

redis:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo update
	helm upgrade --install redis bitnami/redis --set image.tag=7.0.10 --set global.redis.password=123


venv:
	python -m venv venv
	source venv/bin/activate

build-app:
	docker build -t app:1.0.0 . -f app.Dockerfile
	kind load docker-image app:1.0.0

build-consumer:
	docker build -t consumer:1.0.0 consumer -f consumer/consumer.Dockerfile
	kind load docker-image consumer:1.0.0

deploy-app:
	kubectl apply -f app.yaml

deploy-consumer:
	kubectl apply -f consumer.yaml

delete-app:
	kubectl delete -f app.yaml

app-port-forward:
	kubectl port-forward svc/app-service 8000:8000