$apiUrl = "http://localhost:8000/start-task" # 예: http://192.168.49.2:31000/start-task
$requestCount = 100 # 총 100번의 요청을 보냅니다.
$parallelJobs = 10   # 동시에 10개의 요청을 병렬로 보냅니다.

Write-Host "Starting load test on $apiUrl..."
Write-Host "Sending $requestCount requests in parallel batches of $parallelJobs."

$jobScript = {
    param($url)
    Invoke-RestMethod -Uri $url -Method Post
}

for ($i = 0; $i -lt $requestCount; $i += $parallelJobs) {
    $jobs = @()
    for ($j = 0; $j -lt $parallelJobs; $j++) {
        if (($i + $j) -lt $requestCount) {
            $jobs += Start-Job -ScriptBlock $jobScript -ArgumentList $apiUrl
        }
    }
    
    Write-Host "Sent a batch of $($jobs.Count) requests. Waiting for completion..."
    $jobs | Wait-Job | Receive-Job
    $jobs | Remove-Job
    Start-Sleep -Seconds 1 # 각 배치 사이에 1초 대기
}

Write-Host "Load test finished."