# MCP Protokolü ile IoT Kontrolü Kullanımı

> Bu doküman, ESP32 cihazlarında MCP protokolüyle IoT kontrolünün nasıl uygulanacağını açıklar. Ayrıntılı protokol akışı için [`mcp-protocol.md`](./mcp-protocol.md) dosyasına bakın.

## Giriş

MCP (Model Context Protocol), IoT kontrolü için önerilen yeni nesil protokoldür. Standart JSON-RPC 2.0 biçimiyle sunucu ve cihaz arasında araçların keşfedilmesini ve çağrılmasını sağlar. Böylece esnek cihaz kontrolü kurulabilir.

## Tipik Kullanım Akışı

1. Cihaz başlatıldıktan sonra temel protokol üzerinden, örneğin WebSocket veya MQTT ile sunucuya bağlanır.
2. Sunucu, MCP protokolünün `initialize` metoduyla oturumu başlatır.
3. Sunucu, cihazın desteklediği tüm araçları ve parametre açıklamalarını `tools/list` ile alır.
4. Sunucu, belirli bir aracı `tools/call` ile çağırarak cihazı kontrol eder.

Protokol biçimi ve etkileşim ayrıntıları için [`mcp-protocol.md`](./mcp-protocol.md) dosyasına bakın.

## Cihaz Tarafında Araç Kaydı

Cihaz, sunucu tarafından çağrılabilecek araçları `McpServer::AddTool` yöntemiyle kaydeder. Yaygın fonksiyon imzası:

```cpp
void AddTool(
    const std::string& name,           // 工具名称，建议唯一且有层次感，如 self.dog.forward
    const std::string& description,    // 工具描述，简明说明功能，便于大模型理解
    const PropertyList& properties,    // 输入参数列表（可为空），支持类型：布尔、整数、字符串
    std::function<ReturnValue(const PropertyList&)> callback // 工具被调用时的回调实现
);
```

- `name`: Aracın benzersiz kimliği. `modul.islev` benzeri hiyerarşik bir adlandırma önerilir.
- `description`: AI ve kullanıcıların anlayabileceği doğal dil açıklaması.
- `properties`: Parametre listesi. Boş olabilir; bool, integer ve string türlerini destekler. Aralık ve varsayılan değer tanımlanabilir.
- `callback`: Çağrı geldiğinde çalışan gerçek iş mantığıdır. Dönüş değeri `bool`, `int` veya `string` olabilir.

## Tipik Kayıt Örneği

```cpp
void InitializeTools() {
    auto& mcp_server = McpServer::GetInstance();
    // 例1：无参数，控制机器人前进
    mcp_server.AddTool("self.dog.forward", "机器人向前移动", PropertyList(), [this](const PropertyList&) -> ReturnValue {
        servo_dog_ctrl_send(DOG_STATE_FORWARD, NULL);
        return true;
    });
    // 例2：带参数，设置灯光 RGB 颜色
    mcp_server.AddTool("self.light.set_rgb", "设置RGB颜色", PropertyList({
        Property("r", kPropertyTypeInteger, 0, 255),
        Property("g", kPropertyTypeInteger, 0, 255),
        Property("b", kPropertyTypeInteger, 0, 255)
    }), [this](const PropertyList& properties) -> ReturnValue {
        int r = properties["r"].value<int>();
        int g = properties["g"].value<int>();
        int b = properties["b"].value<int>();
        led_on_ = true;
        SetLedColor(r, g, b);
        return true;
    });
}
```

## Yaygın JSON-RPC Araç Çağrısı Örnekleri

### 1. Araç Listesini Alma
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": { "cursor": "" },
  "id": 1
}
```

### 2. Şasiyi İleri Hareket Ettirme
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "self.chassis.go_forward",
    "arguments": {}
  },
  "id": 2
}
```

### 3. Işık Modunu Değiştirme
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "self.chassis.switch_light_mode",
    "arguments": { "light_mode": 3 }
  },
  "id": 3
}
```

### 4. Kamerayı Çevirme
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "self.camera.set_camera_flipped",
    "arguments": {}
  },
  "id": 4
}
```

## Notlar

- Araç adı, parametreler ve dönüş değerleri için cihaz tarafındaki `AddTool` kaydını esas alın.
- Yeni projelerde IoT kontrolü için MCP protokolünün kullanılması önerilir.
- Ayrıntılı protokol ve ileri kullanım için [`mcp-protocol.md`](./mcp-protocol.md) dosyasını inceleyin.
