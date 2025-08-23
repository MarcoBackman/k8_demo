@echo off
REM 사용법:
REM 1. Minikube를 사용하고 있다면, 먼저 FastAPI 서비스의 URL을 확인합니다.
REM    minikube service fastapi-service --url
REM 2. 아래 API_URL 변수에 확인된 URL을 입력합니다.
REM 3. CMD 창에서 `run-load-test.bat` 실행

set API_URL="http://<YOUR-MINIKUBE-IP>:<PORT>/start-task"
set REQUEST_COUNT=100

echo Starting load test on %API_URL%...
echo Sending %REQUEST_COUNT% requests...

FOR /L %%G IN (1,1,%REQUEST_COUNT%) DO (
    echo Sending request %%G...
    REM start /B "Request" curl -X POST %API_URL% > nul 2>&1
    curl -X POST %API_URL%
)

echo Load test finished.
