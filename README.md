# LingTour AI 数字人导游平台

面向中国软件杯 A5「景区导览服务 AI 数字人」赛题的工程骨架。项目采用游客交互端 + 管理后台 + FastAPI 后端 + AI/RAG 服务层的可落地架构，优先完成文本/语音问答、数字人状态、景区知识库、路线推荐、游客感受度报告和数据大屏闭环。

## 参考项目

- [uezo/aiavatarkit](https://github.com/uezo/aiavatarkit)：参考数字人语音对话与角色编排思路。
- [Azure-Samples/rag-postgres-openai-python](https://github.com/Azure-Samples/rag-postgres-openai-python)：参考 FastAPI + PostgreSQL + RAG 的工程组织。
- [SengokuCola/Magic-Voice-Chat](https://github.com/SengokuCola/Magic-Voice-Chat)：参考语音角色聊天的交互链路。
- [guansss/pixi-live2d-display](https://github.com/guansss/pixi-live2d-display)：后续可用于 Live2D Web 展示增强。

## 技术栈

- 前端：Vue 3 + TypeScript + Vite + Pinia + Element Plus + ECharts
- 后端：FastAPI + SQLAlchemy + Pydantic
- AI 服务：RAG 检索、模型适配器、ASR/TTS 占位、情绪分析、路线推荐
- 数据层：PostgreSQL、Redis、Chroma/本地向量库占位
- 部署：Docker Compose

## DeepSeek 多智能体生成器

本项目内置一个轻量 Python 多智能体脚本，用 DeepSeek API 为当前骨架生成架构、后端、前端、AI/RAG、测试文档补齐方案：

```powershell
$env:DEEPSEEK_API_KEY="你的本地 key"
python scripts/deepseek_multi_agent.py --goal "补齐 A5 景区数字人项目骨架"
```

输出目录：

```text
docs/generated/
```

## 快速启动

```powershell
Copy-Item .env.example .env
docker compose -f deploy/docker-compose.yml up --build
```

开发模式：

```powershell
cd backend
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

```powershell
cd frontend
npm install
npm run dev
```

## 核心演示链路

1. 游客创建会话：`POST /api/visitor/sessions`
2. 文本问答：`POST /api/visitor/chat/text`
3. 路线推荐：`POST /api/visitor/routes/recommend`
4. 后台查看数据大屏：`GET /api/admin/analytics/overview`
5. 后台维护知识库与数字人配置
