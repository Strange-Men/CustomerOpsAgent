# Render 环境变量配置说明

## 1. 后端服务

Render 后端地址：

https://customeropsagent.onrender.com

## 2. 必填基础变量

```env
CUSTOMEROPS_ALLOWED_ORIGINS=http://localhost:5173,https://customer-ops-agent.vercel.app
CUSTOMEROPS_LLM_TIMEOUT_SECONDS=30
```

## 3. Mimo Profile 配置

在 Render Dashboard 的 Environment 页面添加：

```env
CUSTOMEROPS_LLM_MIMO_BASE_URL=
CUSTOMEROPS_LLM_MIMO_API_KEY=
CUSTOMEROPS_LLM_MIMO_MODEL=
```

说明：

* `CUSTOMEROPS_LLM_MIMO_BASE_URL` 填 Mimo 的 OpenAI-compatible base URL。
* `CUSTOMEROPS_LLM_MIMO_API_KEY` 填真实 Mimo API key。
* `CUSTOMEROPS_LLM_MIMO_MODEL` 填要调用的模型名。
* 这三个值只能放 Render 后端，不能放 Vercel 前端。
* 如果 Mimo 不是 OpenAI-compatible，需要后续新增专用 adapter。

## 4. Vercel 前端只需要

```env
VITE_API_BASE_URL=https://customeropsagent.onrender.com
```

不要在 Vercel 配置：

* Mimo API key
* DeepSeek API key
* Doubao API key
* 任意 LLM secret

## 5. 配置后验证

配置 Render 环境变量后：

1. 手动 Redeploy Render 服务。
2. 打开：
   https://customeropsagent.onrender.com/docs
3. 在线上前端选择 Mimo：
   https://customer-ops-agent.vercel.app/
4. 提问：
   清关延迟一般是什么原因？
5. 检查：

   * 页面不崩
   * response 中 llm_profile=mimo
   * answer_source 不再只是 mock，除非配置失败 fallback
   * 不泄露 API key

## 6. 安全边界

* `.env` 不能提交。
* `.env.example` 可以提交，但只能写变量名和空值。
* 真实 key 只能在 Render Dashboard 填。
* 前端只传 `llm_profile`。
* 前端不保存 key。
* 前端不允许输入 key。
