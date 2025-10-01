# Test-FlaskUpload.ps1 - 测试Flask视频上传功能

Write-Host "🎯 测试Flask视频上传功能" -ForegroundColor Magenta
Write-Host "=" * 50

# 1. 创建测试视频文件
Write-Host "1. 创建测试视频文件..." -ForegroundColor Cyan
$testVideoPath = "test_video.mp4"
try {
    # 创建一个小的测试文件（模拟视频）
    $fileStream = [System.IO.File]::Create($testVideoPath)
    $fileStream.SetLength(1024 * 1024)  # 1MB
    $fileStream.Close()
    Write-Host "   ✅ 创建测试视频: $testVideoPath (1MB)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ 创建测试视频失败: $($_.Exception.Message)" -ForegroundColor Red
    return
}

# 2. 测试上传API
Write-Host "2. 测试上传API..." -ForegroundColor Cyan
$url = "http://127.0.0.1:5000/upload_video"

try {
    # 使用 multipart/form-data 上传
    $boundary = [System.Guid]::NewGuid().ToString()
    $fileBytes = [System.IO.File]::ReadAllBytes($testVideoPath)
    $enc = [System.Text.Encoding]::GetEncoding("iso-8859-1")
    $fileEnc = $enc.GetString($fileBytes)
    
    $body = @"
--$boundary
Content-Disposition: form-data; name="video"; filename="$testVideoPath"
Content-Type: video/mp4

$fileEnc
--$boundary
Content-Disposition: form-data; name="description"

PowerShell测试视频
--$boundary
Content-Disposition: form-data; name="tags"

测试,自动化,PowerShell
--$boundary--
"@

    $response = Invoke-RestMethod -Uri $url -Method Post -ContentType "multipart/form-data; boundary=$boundary" -Body $body
    Write-Host "   ✅ 上传成功: $($response.message)" -ForegroundColor Green
    
} catch {
    Write-Host "   ❌ 上传失败: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $streamReader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
        $errorResponse = $streamReader.ReadToEnd()
        Write-Host "   错误详情: $errorResponse" -ForegroundColor Red
    }
}

# 3. 清理测试文件
Remove-Item $testVideoPath -ErrorAction SilentlyContinue

# 4. 验证上传结果
Write-Host "3. 验证上传结果..." -ForegroundColor Cyan
try {
    $videos = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/videos/list" -Method GET
    Write-Host "   当前视频数量: $($videos.Count)" -ForegroundColor White
    if ($videos.Count -gt 0) {
        Write-Host "   ✅ 视频上传验证成功!" -ForegroundColor Green
        $videos | Format-Table filename, file_size, upload_time
    } else {
        Write-Host "   ❌ 上传后视频列表仍为空" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ 验证失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "=" * 50
Write-Host "上传测试完成!" -ForegroundColor Magenta
