import streamlit as st
import os
import uuid
from dotenv import load_dotenv

# 尝试导入模型库
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None

try:
    from langchain_community.chat_models import QianfanChatEndpoint
except ImportError:
    QianfanChatEndpoint = None

try:
    from langchain_community.chat_models import ChatOllama
except ImportError:
    ChatOllama = None

try:
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:
    FAISS = None
    OllamaEmbeddings = None
    RecursiveCharacterTextSplitter = None

import tempfile
import os

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import docx2txt
except ImportError:
    docx2txt = None

def process_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def process_docx(file_path):
    return docx2txt.process(file_path)

def process_txt(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def process_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return process_pdf(file_path)
    elif ext == '.docx':
        return process_docx(file_path)
    elif ext == '.txt':
        return process_txt(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {ext}")

# 加载环境变量
load_dotenv()

# 初始化会话状态
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "sessions" not in st.session_state:
    st.session_state.sessions = {st.session_state.session_id: "新会话"}

if "current_session" not in st.session_state:
    st.session_state.current_session = st.session_state.session_id

if "document_store" not in st.session_state:
    st.session_state.document_store = {}

class ModelManager:
    def __init__(self):
        self.model_type = os.getenv('MODEL_TYPE', 'deepseek')
        self.model = self._initialize_model()
    
    def _initialize_model(self):
        if self.model_type == 'ollama':
            if ChatOllama is None:
                raise ValueError("ChatOllama 模块未安装")
            model_name = os.getenv('OLLAMA_MODEL', 'llama3:8b')
            base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            return ChatOllama(model=model_name, base_url=base_url)
        elif self.model_type == 'openai':
            if ChatOpenAI is None:
                raise ValueError("langchain_openai 模块未安装")
            api_key = os.getenv('OPENAI_API_KEY')
            model_name = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
            if not api_key:
                raise ValueError("OPENAI_API_KEY 未配置")
            return ChatOpenAI(api_key=api_key, model=model_name)
        elif self.model_type == 'anthropic':
            if ChatAnthropic is None:
                raise ValueError("langchain_anthropic 模块未安装")
            api_key = os.getenv('ANTHROPIC_API_KEY')
            model_name = os.getenv('ANTHROPIC_MODEL', 'claude-3-opus-20240229')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY 未配置")
            return ChatAnthropic(api_key=api_key, model=model_name)
        elif self.model_type == 'qwen':
            if QianfanChatEndpoint is None:
                raise ValueError("QianfanChatEndpoint 模块未安装")
            access_key = os.getenv('DASHSCOPE_ACCESS_KEY')
            secret_key = os.getenv('DASHSCOPE_SECRET_KEY')
            model_name = os.getenv('QWEN_MODEL', 'qwen2-72b-instruct')
            if not access_key or not secret_key:
                raise ValueError("DASHSCOPE_ACCESS_KEY 和 DASHSCOPE_SECRET_KEY 未配置")
            return QianfanChatEndpoint(
                access_key=access_key, 
                secret_key=secret_key, 
                model=model_name
            )
        elif self.model_type == 'deepseek':
            if ChatOpenAI is None:
                raise ValueError("langchain_openai 模块未安装")
            api_key = os.getenv('DEEPSEEK_API_KEY')
            model_name = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
            base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
            if not api_key:
                raise ValueError("DEEPSEEK_API_KEY 未配置")
            return ChatOpenAI(api_key=api_key, model=model_name, base_url=base_url)
        else:
            from langchain_core.language_models import BaseLanguageModel
            from langchain_core.messages import HumanMessage
            
            class SimpleLocalModel(BaseLanguageModel):
                def _generate(self, messages, stop=None, run_manager=None):
                    last_message = messages[-1]
                    if isinstance(last_message, HumanMessage):
                        content = last_message.content
                        if '你好' in content or 'Hello' in content:
                            return {'generations': [{'text': '你好！我是AI助手。'}]}
                        else:
                            return {'generations': [{'text': f'收到消息：{content}\n\n请配置API密钥以使用完整功能。'}]}
                    return {'generations': [{'text': '我是AI助手。'}]}
            return SimpleLocalModel()
    
    def get_model(self):
        return self.model

# 初始化模型
try:
    model_manager = ModelManager()
    model = model_manager.get_model()
    st.success(f"模型初始化成功: {model_manager.model_type}")
except Exception as e:
    st.error(f"模型初始化失败: {str(e)}")
    st.info("正在使用本地模拟模型...")
    
    from langchain_core.messages import HumanMessage, AIMessage
    
    class SimpleLocalModel:
        def invoke(self, messages):
            if isinstance(messages, list) and len(messages) > 0:
                last_message = messages[-1]
                if isinstance(last_message, HumanMessage):
                    content = last_message.content
                    if '你好' in content or 'Hello' in content:
                        return AIMessage(content='你好！我是AI助手。\n\n注意：当前使用本地模拟模型，如需完整功能，请配置API密钥。')
                    else:
                        return AIMessage(content=f'收到消息：{content}\n\n注意：当前使用本地模拟模型，如需完整功能，请配置API密钥。')
            return AIMessage(content='我是AI助手。')
    
    model = SimpleLocalModel()

# 侧边栏 - 会话管理
with st.sidebar:
    st.title("会话管理")
    
    for session_id, session_name in st.session_state.sessions.items():
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(session_name, key=f"session_{session_id}"):
                st.session_state.current_session = session_id
                st.session_state.messages = []
        with col2:
            if st.button("🗑", key=f"delete_{session_id}"):
                del st.session_state.sessions[session_id]
                if st.session_state.current_session == session_id:
                    new_id = str(uuid.uuid4())
                    st.session_state.sessions[new_id] = "新会话"
                    st.session_state.current_session = new_id
                st.session_state.messages = []
    
    if st.button("创建新会话"):
        new_id = str(uuid.uuid4())
        st.session_state.sessions[new_id] = "新会话"
        st.session_state.current_session = new_id
        st.session_state.messages = []

# 主界面 - 选项卡
tab1, tab2, tab4 = st.tabs(["基本对话", "文档解析", "代码解释"])

# 基本对话
with tab1:
    st.title("AI对话助手")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("请输入您的问题..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        if model:
            from langchain_core.messages import HumanMessage, AIMessage
            
            messages = []
            for item in st.session_state.messages:
                if item["role"] == "user":
                    messages.append(HumanMessage(content=item["content"]))
                else:
                    messages.append(AIMessage(content=item["content"]))
            messages.append(HumanMessage(content=prompt))
            
            try:
                response = model.invoke(messages)
                assistant_response = response.content
            except Exception as e:
                assistant_response = f"API调用失败: {str(e)}"
            
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        else:
            st.error("模型未初始化")

# 文档解析
with tab2:
    st.title("文档解析问答")
    
    uploaded_file = st.file_uploader("上传文档", type=["pdf", "docx", "txt"])
    if uploaded_file:
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name
        
        try:
            text = process_document(temp_file_path)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_text(text)
            
            if st.session_state.current_session not in st.session_state.document_store:
                st.session_state.document_store[st.session_state.current_session] = {
                    "documents": [],
                    "vectorstore": None
                }
            
            embeddings = OllamaEmbeddings(model="llama3:8b")
            vectorstore = FAISS.from_texts(chunks, embeddings)
            
            st.session_state.document_store[st.session_state.current_session]["documents"].append(uploaded_file.name)
            st.session_state.document_store[st.session_state.current_session]["vectorstore"] = vectorstore
            
            st.success(f"文档上传成功: {uploaded_file.name}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
    
    if st.session_state.current_session in st.session_state.document_store:
        docs = st.session_state.document_store[st.session_state.current_session]["documents"]
        if docs:
            st.subheader("已上传的文档:")
            for doc in docs:
                st.write(f"- {doc}")
    
    question = st.text_input("基于文档提问")
    if st.button("提交问题"):
        if st.session_state.current_session not in st.session_state.document_store:
            st.error("请先上传文档")
        else:
            vectorstore = st.session_state.document_store[st.session_state.current_session]["vectorstore"]
            if not vectorstore or not model:
                st.error("文档或模型未准备好")
            else:
                docs = vectorstore.similarity_search(question, k=3)
                context = "\n".join([doc.page_content for doc in docs])
                prompt = f"基于以下文档内容回答问题：\n\n{context}\n\n问题：{question}\n\n回答："
                
                try:
                    response = model.invoke([HumanMessage(content=prompt)])
                    answer = response.content
                except Exception as e:
                    answer = f"API调用失败: {str(e)}"
                
                st.subheader("回答:")
                st.markdown(answer)
                
                st.subheader("来源:")
                for i, doc in enumerate(docs):
                    st.write(f"{i+1}. {doc.page_content[:200]}...")

# 代码解释
with tab4:
    st.title("代码解释")
    
    language = st.selectbox("选择语言", ["Python", "JavaScript", "Java", "C++", "Go", "Rust"])
    code = st.text_area("输入代码", height=300)
    question = st.text_input("额外问题（可选）")
    
    if st.button("解释代码"):
        if not model:
            st.error("模型未初始化")
        else:
            prompt = f"请分析以下{language}代码：\n\n```\n{code}\n```\n\n请提供：\n1. 代码的功能和逻辑解释\n2. 代码的工作原理和实现机制\n3. 代码的改进建议\n4. 代码中潜在的问题和边界情况\n"
            
            if question:
                prompt += f"\n额外问题：{question}\n"
            
            try:
                response = model.invoke([HumanMessage(content=prompt)])
                content = response.content
            except Exception as e:
                content = f"API调用失败: {str(e)}"
            
            st.subheader("代码解释:")
            st.markdown(content)

if __name__ == "__main__":
    pass
