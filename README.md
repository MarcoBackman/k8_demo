# FastAPI & Celery 자동 확장(Auto-scaling) 프로젝트
이 프로젝트는 쿠버네티스 환경에서 트래픽 및 작업 부하에 따라 FastAPI와 Celery Worker Pod 수를 자동으로 조절하는 방법을 보여줍니다.

### **사전 준비**
1. Docker Desktop 또는 Minikube와 같은 로컬 쿠버네티스 클러스터
2. kubectl CLI
3. Docker Hub 계정

## 1단계: Metrics Server 설치 (FastAPI HPA용)
HPA는 Pod의 리소스 사용량을 알아야 합니다. Minikube 환경에서는 아래 명령어로 간단히 활성화할 수 있습니다.

minikube addons enable metrics-server

## 2단계: KEDA 설치 (Celery Worker 스케일링용)
KEDA는 Redis 큐 길이를 모니터링하여 Celery Worker를 확장하는 데 사용됩니다. Helm을 사용하거나 직접 YAML을 적용하여 설치할 수 있습니다.

```
# Helm을 사용하는 경우
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda --namespace keda --create-namespace

# 또는 kubectl로 직접 설치
kubectl apply -f https://github.com/kedacore/keda/releases/download/v2.12.0/keda-2.12.0.yaml
```

## 3단계: Docker 이미지 빌드 및 푸시
1. `fastapi-api/deployment.yaml`과 `celery-worker/deployment.yaml` 파일에서 `your-dockerhub-username`을 본인의 Docker Hub ID로 변경하세요.
2. 프로젝트의 app/ 폴더로 이동합니다.
3. 아래 명령어를 실행하여 이미지를 빌드하고 푸시합니다.

```
# app 폴더 안에서 실행
docker build -t your-dockerhub-username/fastapi-celery-scaler:latest .
docker push your-dockerhub-username/fastapi-celery-scaler:latest
```

## 4단계: 쿠버네티스에 배포
프로젝트의 루트 폴더에서 아래 명령어를 순서대로 실행합니다.

```
# Redis 배포
kubectl apply -f ./redis/

# FastAPI API 배포 (Deployment, Service, HPA)
kubectl apply -f ./fastapi-api/

# Celery Worker 배포 (Deployment, KEDA Scaler)
kubectl apply -f ./celery-worker/
```

## 5단계: 자동 확장(Auto-scaling) 테스트

1. 새 터미널을 열고 Pod와 HPA의 상태를 모니터링합니다. -w 플래그는 변경 사항을 실시간으로 보여줍니다.
```
# Pod 상태 모니터링
kubectl get pods -w

# HPA 상태 모니터링 (CPU 사용량과 Pod 수를 볼 수 있음)
kubectl get hpa -w
```

2. FastAPI 서비스의 외부 접속 URL을 확인합니다.
```
minikube service fastapi-service --url
```
3. `run-load-test.ps1` 또는 `run-load-test.bat` 스크립트를 열어 `$apiUrl` 또는 `API_URL` 변수에 위에서 얻은 URL을 입력합니다.

4. 스크립트를 실행하여 부하를 발생시킵니다.
```
# PowerShell
.\run-load-test.ps1

# Batch
run-load-test.bat
```

5. 모니터링하던 터미널을 확인하세요.

- API 요청이 급증하면서 FastAPI Pod의 CPU 사용량이 늘어나고, HPA가 TARGETS(예: 150%/50%)를 초과하면 새로운 FastAPI Pod가 생성되는 것을 볼 수 있습니다.

- Redis 큐에 작업이 쌓이면 KEDA가 이를 감지하여 Celery Worker Pod를 늘리는 것을 볼 수 있습니다.

- 부하 테스트가 끝나고 일정 시간이 지나면, CPU 사용량과 큐 길이가 줄어들어 Pod 수가 다시 원래대로 돌아가는 것을 확인할 수 있습니다.

## 6단계: 리소스 정리
테스트가 끝나면 아래 명령어로 모든 리소스를 삭제합니다.
```
kubectl delete -f ./celery-worker/
kubectl delete -f ./fastapi-api/
kubectl delete -f ./redis/
```