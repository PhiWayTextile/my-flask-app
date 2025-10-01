# Test-UploadFixed.ps1 - 修复版上传测试

Write-Host "🔄 修复版上传测试" -ForegroundColor Cyan
Write-Host "=" * 50

# 1. 创建测试视频文件
Write-Host "1. 创建测试视频文件..." -ForegroundColor Yellow
$testVideoPath = "test_video.mp4"
try {
    # 创建一个小的测试文件
    $fileContent = [byte[]]::new(1024 * 1024)  # 1MB
    [System.IO.File]::WriteAllBytes($testVideoPath, $fileContent)
    Write-Host "   ✅ 创建测试视频: $testVideoPath (1MB)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ 创建测试视频失败: $($_.Exception.Message)" -ForegroundColor Red
    return
}

# 2. 使用简单的方法测试上传
Write-Host "2. 使用简单方法测试上传..." -ForegroundColor Yellow
$uploadUrl = "http://127.0.0.1:5000/upload_video"

try {
    # 使用 multipart/form-data 上传
    $boundary = [System.Guid]::NewGuid().ToString()
    $LF = "`r`n"
    
    $bodyLines = @(
        "--$boundary",
        "Content-Disposition: form-data; name=`"video`"; filename=`"$testVideoPath`"",
        "Content-Type: video/mp4",
        "",
        [System.IO.File]::ReadAllText($testVideoPath),
        "--$boundary",
        "Content-Disposition: form-data; name=`"description`"",
        "",
        "PowerShell自动化测试视频",
        "--$boundary",
        "Content-Disposition: form-data; name=`"tags`"",
        "",
        "测试,自动化,PowerShell",
        "--$boundary--"
    )
    
    $body = $bodyLines -join $LF
    $contentType = "multipart/form-data; boundary=$boundary"
    
    Write-Host "   上传到: $uploadUrl" -ForegroundColor White
    Write-Host "   内容类型: $contentType" -ForegroundColor Gray
    
    $response = Invoke-WebRequest -Uri $uploadUrl -Method POST -ContentType $contentType -Body $body -TimeoutSec 30
    Write-Host "   ✅ 上传请求成功! 状态码: $($response.StatusCode)" -ForegroundColor Green
    
    # 解析响应
    $responseContent = $response.Content | ConvertFrom-Json
    if ($responseContent.success) {
        Write-Host "   ✅ 上传成功: $($responseContent.message)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ 上传失败: $($responseContent.error)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "   ❌ 上传失败: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        try {
            $streamReader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
            $errorResponse = $streamReader.ReadToEnd()
            Write-Host "   错误响应: $errorResponse" -ForegroundColor Red
        } catch {
            Write-Host "   无法读取错误响应" -ForegroundColor Red
        }
    }
}

# 3. 清理测试文件
Remove-Item $testVideoPath -ErrorAction SilentlyContinue

# 4. 验证上传结果
Write-Host "3. 验证上传结果..." -ForegroundColor Yellow
try {
    $videos = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/videos/list" -Method GET -TimeoutSec 5
    Write-Host "   当前视频数量: $($videos.Count)" -ForegroundColor White
    if ($videos.Count -gt 0) {
        Write-Host "   ✅ 视频上传验证成功!" -ForegroundColor Green
        $videos | Format-Table filename, file_size, upload_time, description
    } else {
        Write-Host "   ❌ 上传后视频列表仍为空" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ 验证失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "=" * 50
Write-Host "修复版上传测试完成!" -ForegroundColor Cyan
