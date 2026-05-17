# VoiaX ESP32 Asistan

VoiaX, ESP32 tabanlı cihazlarda sesli asistan deneyimi sunan açık kaynak bir firmware ve sunucu bütünüdür. Sistem; ASR, LLM, TTS, OTA, MQTT/UDP, WebSocket, MCP ve web panel bileşenleriyle çalışır.

## Özellikler

- Wi-Fi ve ML307 Cat.1 4G desteği
- ESP-SR ile çevrimdışı uyandırma kelimesi algılama
- WebSocket veya MQTT + UDP iletişim protokolü
- OPUS ses kodeği
- Akış tabanlı ASR + LLM + TTS konuşma mimarisi
- Konuşmacı tanıma
- OLED/LCD ekran ve emoji gösterimi
- Pil durumu ve güç yönetimi
- Türkçe cihaz ekran dili
- ESP32-C3, ESP32-S3 ve ESP32-P4 platform desteği
- Cihaz tarafı MCP ile hoparlör, LED, servo ve GPIO kontrolü
- Sunucu tarafı MCP ile akıllı ev, masaüstü kontrolü, Bilgi Tabanı ve eklenti yetenekleri
- Web tabanlı tema, uyandırma kelimesi, font, emoji ve arka plan üretimi

## Sürüm Notu

v2 firmware, v1 partition table ile uyumlu değildir. v1’den v2’ye OTA ile doğrudan geçiş yapılamaz; v2’ye geçiş için firmware’in elle flash edilmesi gerekir. Partition ayrıntıları için [partitions/v2/README.md](partitions/v2/README.md) dosyasına bakın.

## Donanım

VoiaX çok sayıda ESP32 tabanlı açık kaynak kartı destekler. Yaygın örnekler:

- Espressif ESP32-S3-BOX3
- M5Stack CoreS3
- M5Stack AtomS3R + Echo Base
- Waveshare ESP32-S3-Touch-AMOLED-1.8
- LILYGO T-Circle-S3
- Movecall CuiCan AI Pendant
- SenseCAP Watcher
- Breadboard tabanlı ESP32-S3 deneme kartları

Özel kart eklemek için [docs/custom-board.md](docs/custom-board.md) dosyasını kullanın.

## Firmware Yükleme

Geliştirme ortamı kurmadan test etmek için hazır firmware yükleme yöntemi önerilir. Geliştirici olarak derleme yapacaksanız:

- ESP-IDF 5.4 veya üzeri kullanın.
- VSCode veya Cursor üzerinde ESP-IDF eklentisini kurun.
- Linux ortamı derleme ve sürücü sorunları açısından daha kararlıdır.
- Firmware’de teknik path, class, function ve config key adlarını değiştirmeyin.

## Sunucu ve Web Panel

VoiaX Sunucu; Python arka uç, manager-api, manager-web, MySQL, Redis ve MQTT gateway bileşenleriyle çalışır. Web panelden asistan, model sağlayıcı, ASR, TTS, VAD, VLLM, Bilgi Tabanı, eklenti ve OTA ayarları yönetilir.

Yerel yapılandırma için:

- `xiaozhi-esp32-server/main/xiaozhi-server/config.yaml`
- `xiaozhi-esp32-server/main/xiaozhi-server/config_from_api.yaml`

Canlı kurulumlarda secret değerleri `data/.config.yaml`, environment variable veya panel/DB üzerinden yönetilmelidir. Secret ve API key değerlerini loglara veya dokümanlara yazmayın.

## LLM Sağlayıcıları

GitHub Models veya Azure inference benzeri OpenAI uyumlu sağlayıcılar için panelde model tipi `LLM`, provider/type `openai`, `base_url`, `model_name` ve `api_key` alanları yapılandırılır. `model_name` sağlayıcının beklediği tam model adı olmalıdır.

## Geliştirici Dokümanları

- [MCP IoT Kullanımı](docs/mcp-usage.md)
- [MCP Protokol Akışı](docs/mcp-protocol.md)
- [MQTT + UDP Protokolü](docs/mqtt-udp.md)
- [WebSocket Protokolü](docs/websocket.md)
- [Özel Kart Kılavuzu](docs/custom-board.md)

## Açık Kaynak

Bu proje MIT lisansı altında yayımlanır. Teknik upstream repo, protokol ve dosya adlarında `xiaozhi` kullanımları korunabilir; kullanıcıya görünen ürün adı VoiaX’tir.
