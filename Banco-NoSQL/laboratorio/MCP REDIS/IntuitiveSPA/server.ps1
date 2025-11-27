# Servidor HTTP simples em PowerShell
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8080/")
$listener.Start()

Write-Host "🚀 Servidor HTTP iniciado em http://localhost:8080"
Write-Host "📁 Servindo arquivos do diretório atual"
Write-Host "🌐 Acesse: http://localhost:8080/index.html"
Write-Host "⏹️  Pressione Ctrl+C para parar"

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        $url = $request.Url.AbsolutePath
        if ($url -eq "/") { $url = "/index.html" }
        
        $filepath = Join-Path (Get-Location) $url.TrimStart('/')
        
        Write-Host "📥 Requisição: $($request.HttpMethod) $url"
        
        if (Test-Path $filepath) {
            $content = Get-Content $filepath -Raw -Encoding UTF8
            $response.ContentLength64 = [System.Text.Encoding]::UTF8.GetByteCount($content)
            
            # Definir Content-Type
            if ($filepath.EndsWith(".html")) {
                $response.ContentType = "text/html; charset=utf-8"
            } elseif ($filepath.EndsWith(".js")) {
                $response.ContentType = "application/javascript; charset=utf-8"
            } elseif ($filepath.EndsWith(".css")) {
                $response.ContentType = "text/css; charset=utf-8"
            }
            
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($content)
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
        } else {
            $response.StatusCode = 404
            $errorContent = "404 - Arquivo não encontrado: $url"
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($errorContent)
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
        }
        
        $response.Close()
    }
} catch {
    Write-Host "❌ Erro: $_"
} finally {
    $listener.Stop()
}