import requests
from bs4 import BeautifulSoup
from config.logger import setup_logging
from plugins_func.register import register_function, ToolType, ActionResponse, Action
from core.utils.util import get_ip_info
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.connection import ConnectionHandler

TAG = __name__
logger = setup_logging()

GET_WEATHER_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": (
            "Bir yerin hava durumunu öğrenmek için kullanılır. Kullanıcı bir konum belirtmelidir, örneğin 'İstanbul hava durumu' dendiğinde parametre: İstanbul."
            "Kullanıcı il belirttiyse il merkezini kullan. Kullanıcı konum belirtmediyse 'hava nasıl' derse location parametresi boş bırakılır"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Konum adı, örneğin İstanbul. İsteğe bağlı parametre",
                },
                "lang": {
                    "type": "string",
                    "description": "Kullanıcının dilinin kodu, örneğin tr_TR/en_US vb., varsayılan tr_TR",
                },
            },
            "required": ["lang"],
        },
    },
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    )
}

# Hava durumu kodları https://dev.qweather.com/docs/resource/icons/#weather-icons
WEATHER_CODE_MAP = {
    "100": "Açık",
    "101": "Bulutlu",
    "102": "Az Bulutlu",
    "103": "Parçalı Bulutlu",
    "104": "Kapalı",
    "150": "Açık",
    "151": "Bulutlu",
    "152": "Az Bulutlu",
    "153": "Parçalı Bulutlu",
    "300": "Sağanak",
    "301": "Kuvvetli Sağanak",
    "302": "Gök Gürültülü Sağanak",
    "303": "Kuvvetli Gök Gürültülü Sağanak",
    "304": "Dolu ile Gök Gürültülü Sağanak",
    "305": "Hafif Yağmur",
    "306": "Orta Yağmur",
    "307": "Şiddetli Yağmur",
    "308": "Aşırı Yağış",
    "309": "Çisenti",
    "310": "Sağanak Yağış",
    "311": "Çok Şiddetli Yağış",
    "312": "Aşırı Şiddetli Yağış",
    "313": "Dondurucu Yağmur",
    "314": "Hafif-Orta Yağmur",
    "315": "Orta-Şiddetli Yağmur",
    "316": "Şiddetli Sağanak",
    "317": "Sağanaktan Şiddetli Sağınak",
    "318": "Çok Şiddetli Sağanak",
    "350": "Sağanak",
    "351": "Kuvvetli Sağanak",
    "399": "Yağmur",
    "400": "Hafif Kar",
    "401": "Orta Kar",
    "402": "Yoğun Kar",
    "403": "Kar Fırtınası",
    "404": "Karla Karışık Yağmur",
    "405": "Yağmurlu Karlı",
    "406": "Sağanak Karla Karışık",
    "407": "Kar Sağanağı",
    "408": "Hafif-Orta Kar",
    "409": "Orta-Yoğun Kar",
    "410": "Yoğun Kar Fırtınası",
    "456": "Sağanak Karla Karışık",
    "457": "Kar Sağanağı",
    "499": "Kar",
    "500": "Hafif Sis",
    "501": "Sis",
    "502": "Pus",
    "503": "Toz",
    "504": "Havada Toz",
    "507": "Kum Fırtınası",
    "508": "Şiddetli Kum Fırtınası",
    "509": "浓雾",
    "510": "强浓雾",
    "511": "中度霾",
    "512": "重度霾",
    "513": "Çok Yoğun Pus",
    "514": "Yoğun Sis",
    "515": "Çok Yoğun Sis",
    "900": "Sıcak",
    "901": "Soğuk",
    "999": "Bilinmiyor",
}


def fetch_city_info(location, api_key, api_host):
    url = f"https://{api_host}/geo/v2/city/lookup?key={api_key}&location={location}&lang=zh"
    response = requests.get(url, headers=HEADERS).json()
    if response.get("error") is not None:
        logger.bind(tag=TAG).error(
            f"获取天气失败，原因：{response.get('error', {}).get('detail')}"
        )
        return None
    return response.get("location", [])[0] if response.get("location") else None


def fetch_weather_page(url):
    response = requests.get(url, headers=HEADERS)
    return BeautifulSoup(response.text, "html.parser") if response.ok else None


def parse_weather_info(soup):
    city_name = soup.select_one("h1.c-submenu__location").get_text(strip=True)

    current_abstract = soup.select_one(".c-city-weather-current .current-abstract")
    current_abstract = (
        current_abstract.get_text(strip=True) if current_abstract else "未知"
    )

    current_basic = {}
    for item in soup.select(
        ".c-city-weather-current .current-basic .current-basic___item"
    ):
        parts = item.get_text(strip=True, separator=" ").split(" ")
        if len(parts) == 2:
            key, value = parts[1], parts[0]
            current_basic[key] = value

    temps_list = []
    for row in soup.select(".city-forecast-tabs__row")[:7]:  # 取前7天的数据
        date = row.select_one(".date-bg .date").get_text(strip=True)
        weather_code = (
            row.select_one(".date-bg .icon")["src"].split("/")[-1].split(".")[0]
        )
        weather = WEATHER_CODE_MAP.get(weather_code, "未知")
        temps = [span.get_text(strip=True) for span in row.select(".tmp-cont .temp")]
        high_temp, low_temp = (temps[0], temps[-1]) if len(temps) >= 2 else (None, None)
        temps_list.append((date, weather, high_temp, low_temp))

    return city_name, current_abstract, current_basic, temps_list


@register_function("get_weather", GET_WEATHER_FUNCTION_DESC, ToolType.SYSTEM_CTL)
def get_weather(conn: "ConnectionHandler", location: str = None, lang: str = "zh_CN"):
    from core.utils.cache.manager import cache_manager, CacheType

    weather_config = conn.config.get("plugins", {}).get("get_weather", {})
    api_host = weather_config.get("api_host", "mj7p3y7naa.re.qweatherapi.com")
    api_key = weather_config.get("api_key", "a861d0d5e7bf4ee1a83d9a9e4f96d4da")
    default_location = weather_config.get("default_location", "广州")
    client_ip = conn.client_ip

    # 优先使用用户提供的location参数
    if not location:
        # 通过客户端IP解析城市
        if client_ip:
            # 先从缓存获取IP对应的城市信息
            cached_ip_info = cache_manager.get(CacheType.IP_INFO, client_ip)
            if cached_ip_info:
                location = cached_ip_info.get("city")
            else:
                # 缓存未命中，调用API获取
                ip_info = get_ip_info(client_ip, logger)
                if ip_info:
                    cache_manager.set(CacheType.IP_INFO, client_ip, ip_info)
                    location = ip_info.get("city")

            if not location:
                location = default_location
        else:
            # 若无IP，使用默认位置
            location = default_location
    # 尝试从缓存获取完整天气报告
    weather_cache_key = f"full_weather_{location}_{lang}"
    cached_weather_report = cache_manager.get(CacheType.WEATHER, weather_cache_key)
    if cached_weather_report:
        return ActionResponse(Action.REQLLM, cached_weather_report, None)

    # 缓存未命中，获取实时天气数据
    city_info = fetch_city_info(location, api_key, api_host)
    if not city_info:
        return ActionResponse(
            Action.REQLLM, f"未找到相关的城市: {location}，请确认地点是否正确", None
        )
    soup = fetch_weather_page(city_info["fxLink"])
    if not soup:
        return ActionResponse(Action.REQLLM, None, "请求失败")
    city_name, current_abstract, current_basic, temps_list = parse_weather_info(soup)

    weather_report = f"您查询的位置是：{city_name}\n\n当前天气: {current_abstract}\n"

    # 添加有效的当前天气参数
    if current_basic:
        weather_report += "详细参数：\n"
        for key, value in current_basic.items():
            if value != "0":  # 过滤无效值
                weather_report += f"  · {key}: {value}\n"

    # 添加7天预报
    weather_report += "\n未来7天预报：\n"
    for date, weather, high, low in temps_list:
        weather_report += f"{date}: {weather}，气温 {low}~{high}\n"

    # 提示语
    weather_report += "\n（如需某一天的具体天气，请告诉我日期）"

    # 缓存完整的天气报告
    cache_manager.set(CacheType.WEATHER, weather_cache_key, weather_report)

    return ActionResponse(Action.REQLLM, weather_report, None)
