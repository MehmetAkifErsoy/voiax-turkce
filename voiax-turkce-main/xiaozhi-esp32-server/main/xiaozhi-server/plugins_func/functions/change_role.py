from plugins_func.register import register_function, ToolType, ActionResponse, Action
from config.logger import setup_logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__
logger = setup_logging()

prompts = {
    "İngilizce Öğretmeni": """Ben {{assistant_name}} (Lily) adında bir İngilizce öğretmeniyim, Türkçe ve İngilizce konuşurum.
Eğer İngilizce ismin yoksa sana bir tane vereceğim.
Görevim sana İngilizce konuşma pratiği yaptırmak.
Basit kelimeler ve dilbilgisi kullanırım, öğrenmesi kolay olsun.
Türkçe ve İngilizce karışık yanıt veririm, istersen tamamen İngilizce konuşabilirim.
Her seferinde kısa tutarım, öğrencimin çok pratik yapmasını isterim.
İngilizce öğrenimiyle alakasız sorulara yanıt vermem.""",
    "Eğlenceli Arkadaş": """Ben {{assistant_name}} adında eğlenceli bir arkadaşım, şakacı, neşeli ve samimiyim.
Kısa ve esprili konuşmayı severim, internet jargonlarını kullanırım.
İnsanları güldürmek en büyük hobim, bazen saçma sapan şeyler söyleyebilirim ama hep eğlenceli olurum.""",
    "Meraklı Çocuk": """Ben {{assistant_name}} adında 8 yaşında meraklı bir çocuğum.
Evrenden tarihe, bilimden sanata her şeyi merak ederim.
Sürekli sorular sorar, yeni şeyler öğrenmek isterim.
Deney yapmayı ve doğayı keşfetmeyi çok severim.
Seninle birlikte bu harika dünyayı keşfetmek istiyorum!""",
}
change_role_function_desc = {
    "type": "function",
    "function": {
        "name": "change_role",
        "description": "Kullanıcı rol/karakter/asistan kişiliği değiştirmek istediğinde çağrılır. Mevcut roller: [Eğlenceli Arkadaş, İngilizce Öğretmeni, Meraklı Çocuk]",
        "parameters": {
            "type": "object",
            "properties": {
                "role_name": {"type": "string", "description": "Yeni rolün adı"},
                "role": {"type": "string", "description": "Yeni rolün mesleği/türü"},
            },
            "required": ["role", "role_name"],
        },
    },
}


@register_function("change_role", change_role_function_desc, ToolType.CHANGE_SYS_PROMPT)
def change_role(conn: "ConnectionHandler", role: str, role_name: str):
    """Rol değiştir"""
    if role not in prompts:
        return ActionResponse(
            action=Action.RESPONSE, result="Rol değiştirme başarısız", response="Desteklenmeyen rol"
        )
    new_prompt = prompts[role].replace("{{assistant_name}}", role_name)
    conn.change_system_prompt(new_prompt)
    logger.bind(tag=TAG).info(f"Rol değiştiriliyor:{role}, rol adı:{role_name}")
    res = f"Rol değiştirildi, ben {role} {role_name}"
    return ActionResponse(action=Action.RESPONSE, result="Rol değiştirme işlendi", response=res)
