import os
import sys

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.insert(0, project_root)

from config.logger import setup_logging
import importlib

logger = setup_logging()


def create_instance(class_name, *args, **kwargs):
    # Web panel type adı → dizin eşlemesi
    type_mapping = {
        "LLM_OpenAI": "openai",
        "LLM_Gemini": "gemini",
        "LLM_Dify": "dify",
        "LLM_Ollama": "ollama",
    }
    class_name = type_mapping.get(class_name, class_name)
    # LLM örneği oluştur
    if os.path.exists(os.path.join('core', 'providers', 'llm', class_name, f'{class_name}.py')):
        lib_name = f'core.providers.llm.{class_name}.{class_name}'
        if lib_name not in sys.modules:
            sys.modules[lib_name] = importlib.import_module(f'{lib_name}')
        return sys.modules[lib_name].LLMProvider(*args, **kwargs)

    raise ValueError(f"不支持的LLM类型: {class_name}，请检查该配置的type是否设置正确")
