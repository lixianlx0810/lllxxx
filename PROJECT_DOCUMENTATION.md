# AI对话助手项目文档

## 项目结构

```
ai-chat-assistant/
├── backend/            # 后端服务目录
│   ├── main.py         # FastAPI主应用
│   ├── model_manager.py # 模型管理器
│   ├── document_qa.py   # 文档问答功能
│   ├── search.py        # 联网搜索功能
│   └── code_interpreter.py # 代码解释功能
├── frontend/           # 前端应用目录
│   ├── app.py          # Streamlit前端应用
│   └── .streamlit/     # Streamlit配置
├── utils/              # 工具函数目录
│   ├── document_processor.py # 文档处理工具
│   └── search_tool.py  # 搜索工具
├── dist/               # 打包输出目录
│   └── AI Chat Assistant.exe # 可执行文件
├── venv/               # 虚拟环境
├── .env                # 环境配置文件
├── .env.example        # 环境配置示例
├── requirements.txt     # 依赖项列表
├── main.py             # 主入口文件
├── start.bat           # Windows启动脚本
├── start.sh            # Linux/Mac启动脚本
└── README.md           # 项目说明
```

## 文件功能说明

### 后端文件

#### `backend/main.py`
- **功能**：FastAPI主应用，处理HTTP请求
- **主要功能**：
  - 提供对话API端点 (`/api/chat`)
  - 管理对话历史 (`/api/history/{session_id}`)
  - 创建新会话 (`/api/create-session`)
  - 配置CORS中间件，允许跨域请求
  - 初始化AI模型

#### `backend/model_manager.py`
- **功能**：模型管理器，负责初始化和管理AI模型
- **支持的模型**：
  - Ollama (本地模型)
  - OpenAI (GPT系列模型)
  - Anthropic (Claude系列模型)
  - 通义千问 (Qwen模型)
  - DeepSeek (深度求索模型)
  - 本地模拟模型 (无API密钥时使用)
- **核心方法**：
  - `_initialize_model()`: 根据配置初始化相应的模型
  - `get_model()`: 获取模型实例

#### `backend/document_qa.py`
- **功能**：文档问答功能
- **主要功能**：
  - 处理文档上传
  - 解析文档内容
  - 基于文档内容回答问题
  - 管理用户上传的文档

#### `backend/search.py`
- **功能**：联网搜索功能
- **主要功能**：
  - 执行网络搜索
  - 处理搜索结果
  - 基于搜索结果生成回答

#### `backend/code_interpreter.py`
- **功能**：代码解释功能
- **主要功能**：
  - 分析代码语法和逻辑
  - 解释代码功能
  - 提供代码改进建议

### 前端文件

#### `frontend/app.py`
- **功能**：Streamlit前端应用
- **主要功能**：
  - 提供用户界面
  - 管理会话
  - 显示对话历史
  - 提供四个功能选项卡：
    - 基本对话
    - 文档解析
    - 联网搜索
    - 代码解释
  - 与后端API通信

#### `frontend/.streamlit/config.toml`
- **功能**：Streamlit配置文件
- **主要配置**：
  - 禁用使用统计
  - 其他Streamlit相关配置

### 工具文件

#### `utils/document_processor.py`
- **功能**：文档处理工具
- **支持的文件类型**：
  - PDF文件
  - Word文档 (.docx)
  - 文本文件 (.txt)
- **核心函数**：
  - `process_pdf()`: 处理PDF文件
  - `process_docx()`: 处理Word文档
  - `process_txt()`: 处理文本文件
  - `split_document()`: 分割文档为小块

#### `utils/search_tool.py`
- **功能**：搜索工具
- **主要功能**：
  - 执行Google搜索
  - 抓取网页内容
  - 处理搜索结果
- **核心函数**：
  - `google_search()`: 执行Google搜索
  - `scrape_webpage()`: 抓取网页内容
  - `search_and_scrape()`: 搜索并抓取网页

### 配置文件

#### `.env`
- **功能**：环境配置文件
- **主要配置项**：
  - 模型类型 (`MODEL_TYPE`)
  - 各模型的API密钥
  - 模型参数配置
  - 搜索API配置

#### `.env.example`
- **功能**：环境配置示例文件
- **作用**：提供配置模板，指导用户如何配置环境变量

#### `requirements.txt`
- **功能**：依赖项列表
- **包含的主要依赖**：
  - fastapi: 后端Web框架
  - uvicorn: ASGI服务器
  - langchain: LLM集成框架
  - streamlit: 前端框架
  - pdfplumber: PDF处理
  - docx2txt: Word文档处理
  - requests: HTTP请求
  - beautifulsoup4: 网页解析
  - faiss-cpu: 向量数据库
  - python-dotenv: 环境变量管理

### 启动和打包文件

#### `main.py`
- **功能**：主入口文件
- **主要功能**：
  - 启动后端服务
  - 启动前端服务
  - 自动打开浏览器

#### `start.bat`
- **功能**：Windows启动脚本
- **主要功能**：
  - 安装依赖
  - 启动后端服务
  - 启动前端服务

#### `start.sh`
- **功能**：Linux/Mac启动脚本
- **主要功能**：
  - 安装依赖
  - 启动后端服务
  - 启动前端服务

#### `AI Chat Assistant.exe`
- **功能**：打包后的可执行文件
- **特点**：
  - 独立可执行文件
  - 包含所有依赖项
  - 一键启动应用

## 技术栈

### 后端
- **框架**：FastAPI
- **服务器**：Uvicorn
- **AI集成**：LangChain
- **向量数据库**：FAISS

### 前端
- **框架**：Streamlit
- **UI组件**：Streamlit内置组件

### 工具
- **文档处理**：pdfplumber, docx2txt
- **网络请求**：requests
- **网页解析**：beautifulsoup4

### 打包
- **工具**：PyInstaller
- **输出**：独立可执行文件

## 使用流程

1. **配置环境**：
   - 编辑 `.env` 文件，选择模型类型并配置相应的API密钥

2. **启动应用**：
   - 双击 `AI Chat Assistant.exe` 文件
   - 或运行 `start.bat` (Windows) 或 `start.sh` (Linux/Mac)

3. **使用功能**：
   - **基本对话**：与AI进行日常对话
   - **文档解析**：上传文档并基于文档提问
   - **联网搜索**：执行网络搜索并获取回答
   - **代码解释**：输入代码并获取解释和改进建议

## 扩展和定制

### 添加新模型
1. 在 `model_manager.py` 中添加新模型的导入和初始化逻辑
2. 在 `.env` 文件中添加相应的配置项

### 添加新功能
1. 在后端添加新的API端点
2. 在前端添加相应的UI组件
3. 更新相关工具函数

### 定制界面
1. 修改 `frontend/app.py` 文件
2. 调整Streamlit组件和布局

## 故障排除

### 常见问题

1. **端口被占用**：
   - 错误信息：`error while attempting to bind on address ('0.0.0.0', 8000)`
   - 解决方案：终止占用端口的进程，或修改配置文件中的端口

2. **模型初始化失败**：
   - 错误信息：`模型未初始化`
   - 解决方案：检查API密钥配置，确保网络连接正常

3. **文档上传失败**：
   - 错误信息：`上传失败`
   - 解决方案：检查文件大小，确保文件格式正确

4. **搜索功能不工作**：
   - 错误信息：`搜索失败`
   - 解决方案：检查网络连接，确保搜索API配置正确

## 总结

AI对话助手是一个功能丰富的智能对话应用，支持多种AI模型，提供文档解析、联网搜索和代码解释等功能。项目采用前后端分离架构，使用现代Python技术栈构建，具有良好的扩展性和可定制性。

通过配置不同的模型和API密钥，用户可以根据自己的需求选择合适的AI服务，实现从简单的本地对话到复杂的文档分析和代码解释等多种功能。