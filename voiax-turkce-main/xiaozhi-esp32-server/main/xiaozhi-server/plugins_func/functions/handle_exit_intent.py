from plugins_func.register import register_function, ToolType, ActionResponse, Action
from config.logger import setup_logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__
logger = setup_logging()

handle_exit_intent_function_desc = {
    "type": "function",
    "function": {
        "name": "handle_exit_intent",
        "description": "Kullanıcı sohbeti bitirmek veya sistemden çıkmak istediğinde çağrılır",
        "parameters": {
            "type": "object",
            "properties": {
                "say_goodbye": {
                    "type": "string",
                    "description": "Kullanıcıyla samimi bir veda mesajı",
                }
            },
            "required": ["say_goodbye"],
        },
    },
}


@register_function(
    "handle_exit_intent", handle_exit_intent_function_desc, ToolType.SYSTEM_CTL
)
def handle_exit_intent(conn: "ConnectionHandler", say_goodbye: str | None = None):
    conn.is_exiting = True
    # 处理退出意图
    try:
        if say_goodbye is None:
            say_goodbye = "Görüşürüz, iyi günler!"
        conn.close_after_chat = True
        logger.bind(tag=TAG).info(f"Çıkış niyeti işlendi:{say_goodbye}")
        return ActionResponse(
            action=Action.RESPONSE, result="Çıkış niyeti işlendi", response=say_goodbye
        )
    except Exception as e:
        logger.bind(tag=TAG).error(f"Çıkış niyeti işlenirken hata: {e}")
        return ActionResponse(
            action=Action.NONE, result="Çıkış niyeti işlenemedi", response=""
        )
