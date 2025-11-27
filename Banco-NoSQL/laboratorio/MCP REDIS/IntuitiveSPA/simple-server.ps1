# Servidor HTTP simples
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8080/")
$listener.Start()

Write-Host "🚀 Servidor HTTP rodando em http://localhost:8080"
Write-Host "🌐 Acesse: http://localhost:8080"

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    
    $url = $request.Url.AbsolutePath
    if ($url -eq "/") { $url = "/index.html" }
    
    $filepath = Join-Path (Get-Location) $url.TrimStart('/')
    
    Write-Host "📥 $($request.HttpMethod) $url"
    
    if (Test-Path $filepath) {
        $content = [System.IO.File]::ReadAllText($filepath, [System.Text.Encoding]::UTF8)
        $response.ContentType = "text/html; charset=utf-8"
        $buffer = [System.Text.Encoding]::UTF8.GetBytes($content)
        $response.ContentLength64 = $buffer.Length
        $response.OutputStream.Write($buffer, 0, $buffer.Length)
    } else {
        $response.StatusCode = 404
        $errorContent = "404 - Not Found"
        $buffer = [System.Text.Encoding]::UTF8.GetBytes($errorContent)
        $response.OutputStream.Write($buffer, 0, $buffer.Length)
    }
    
    $response.Close()
}