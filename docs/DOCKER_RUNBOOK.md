# Docker 本地运行手册

## 目标

通过 Docker Compose 在本地一键运行 CustomerOpsAgent 前后端，无需手动安装 Python/Node 环境。

## 前置要求

- Docker Desktop（Windows / macOS / Linux）
- docker compose（Docker Desktop 自带）

## 快速启动

```bash
# 构建镜像（首次或依赖变更时）
docker compose build --no-cache

# 启动服务（后台运行）
docker compose up -d
```

## 访问地址

| 服务 | 地址 |
|------|------|
| Frontend | http://localhost:8080 |
| Backend API Docs | http://localhost:8000/docs |

## API Smoke 测试

```bash
curl -X POST "http://localhost:8000/api/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "清关延迟一般是什么原因？",
    "order_id": null,
    "conversation_history": [],
    "llm_profile": "mock"
  }'
```

PowerShell 版本：

```powershell
$body = @{
    user_query = "清关延迟一般是什么原因？"
    order_id = $null
    conversation_history = @()
    llm_profile = "mock"
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
  -Uri "http://localhost:8000/api/agent/chat" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

## 停止服务

```bash
docker compose down
```

## 查看日志

```bash
# 后端日志
docker compose logs backend --tail=120

# 前端日志
docker compose logs frontend --tail=120
```

## 环境变量说明

Docker Compose 默认使用 mock 模式，无需真实 LLM key。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PYTHONPATH` | `/app/backend` | 后端 Python 模块路径 |
| `CUSTOMEROPS_ALLOWED_ORIGINS` | `http://localhost:5173,http://localhost:8080,...` | CORS 允许的来源 |
| `CUSTOMEROPS_LLM_TIMEOUT_SECONDS` | `30` | LLM 请求超时 |
| `VITE_API_BASE_URL` | `http://localhost:8000` | 前端调用后端的地址（构建时注入） |

真实 LLM key（Mimo / DeepSeek / Doubao）不写入 `docker-compose.yml`，需通过 Render 线上环境变量配置。

## 常见问题

### 端口被占用

如果 8000 或 8080 端口被占用：

```bash
# 查看占用端口的进程
netstat -ano | findstr :8000
netstat -ano | findstr :8080
```

修改 `docker-compose.yml` 中的端口映射，例如改为 `"8001:8000"`。

### Docker Desktop 未启动

启动 Docker Desktop，等待状态栏显示 "Docker Desktop is running" 后重试。

### CORS 错误

确认 `CUSTOMEROPS_ALLOWED_ORIGINS` 包含你访问前端的地址。默认已包含 `http://localhost:8080`。

### VITE_API_BASE_URL 不生效

该变量在构建时注入。如果修改了值，需要重新构建：

```bash
docker compose build --no-cache frontend
docker compose up -d
```

### PYTHONPATH 问题

如果后端报 `ModuleNotFoundError`，确认 `PYTHONPATH=/app/backend` 环境变量已设置。

## 安全边界

- `.env` 文件不打入 Docker 镜像（已在 `.dockerignore` 排除）。
- 真实 API key 不写入 `Dockerfile` 或 `docker-compose.yml`。
- 前端不注入任何后端 key。
- 默认使用 mock profile，无需真实 LLM key 即可运行。
