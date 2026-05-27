# AI智能聊天助手

一款集成式AI助手应用，支持多种大模型，提供对话、文档解析、代码解释等功能。

## 技术栈

- **后端**: FastAPI / Python
- **前端**: Streamlit
- **LLM框架**: LangChain
- **打包工具**: PyInstaller

## 功能特性

- ✅ **基本对话**: 支持多轮交互与上下文记忆
- ✅ **文档解析**: 支持PDF、Word、TXT文件上传与问答
- ✅ **联网搜索**: 集成在线搜索能力（需配置）
- ✅ **代码解释**: 支持Python、JavaScript、Java、C++、Go、Rust等语言

## 支持的模型

| 模型类型 | 配置方式 |
|---------|---------|
| DeepSeek | `MODEL_TYPE=deepseek` |
| OpenAI | `MODEL_TYPE=openai` |
| Anthropic | `MODEL_TYPE=anthropic` |
| Qwen | `MODEL_TYPE=qwen` |
| Ollama | `MODEL_TYPE=ollama` |

## 快速开始

### 本地运行

1. **安装依赖**
```bash
cd ai-chat-assistant
pip install -r requirements.txt
```

2. **配置环境变量**
编辑 `.env` 文件，设置API密钥：
```
MODEL_TYPE=deepseek
DEEPSEEK_API_KEY=your_api_key
```

3. **启动服务**

方式一：使用前后端分离模式
```bash
# 启动后端
cd backend
python main.py

# 启动前端（新终端）
cd frontend
streamlit run app.py
```

方式二：使用单文件模式
```bash
streamlit run streamlit_app.py
```

### 访问地址

- 前端: http://localhost:8501
- 后端API: http://localhost:8000

## Streamlit Community Cloud 部署

### 步骤

1. **创建GitHub仓库**
   - 将代码推送到GitHub仓库

2. **配置Secrets**
   在 Streamlit Community Cloud 中添加以下 Secrets：
   ```toml
   MODEL_TYPE = "deepseek"
   DEEPSEEK_API_KEY = "your_api_key"
   DEEPSEEK_MODEL = "deepseek-chat"
   DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
   ```

3. **部署**
   - 访问 [share.streamlit.io](https://share.streamlit.io/)
   - 连接你的GitHub仓库
   - 指定主文件为 `streamlit_app.py`
   - 点击部署

## 项目结构

```
ai-chat-assistant/
├── backend/              # 后端服务
│   ├── main.py           # FastAPI主应用
│   ├── model_manager.py  # 模型管理
│   ├── document_qa.py    # 文档问答
│   ├── search.py         # 搜索功能
│   └── code_interpreter.py # 代码解释
├── frontend/             # 前端应用
│   └── app.py            # Streamlit应用
├── utils/                # 工具函数
│   ├── document_processor.py
│   └── search_tool.py
├── streamlit_app.py      # 单文件部署版本
├── requirements.txt      # 依赖列表
├── .env                  # 环境变量配置
└── .streamlit/           # Streamlit配置
    └── secrets.toml      # 云部署配置
```

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|-------|------|-------|
| MODEL_TYPE | 模型类型 | deepseek |
| DEEPSEEK_API_KEY | DeepSeek API密钥 | - |
| DEEPSEEK_MODEL | DeepSeek模型名 | deepseek-chat |
| DEEPSEEK_BASE_URL | DeepSeek API地址 | https://api.deepseek.com/v1 |
| OPENAI_API_KEY | OpenAI API密钥 | - |
| ANTHROPIC_API_KEY | Anthropic API密钥 | - |
| DASHSCOPE_API_KEY | 通义千问API密钥 | - |
| GOOGLE_API_KEY | Google搜索API密钥 | - |
| GOOGLE_CSE_ID | Google搜索引擎ID | - |

## 许可证

MIT License
