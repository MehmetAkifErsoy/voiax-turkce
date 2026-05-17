# Özel Geliştirme Kartı Kılavuzu

Bu kılavuz, VoiaX ESP32 firmware projesine yeni bir geliştirme kartı ekleme akışını açıklar. VoiaX, farklı ESP32 serisi kartların başlatma kodlarını ilgili kart dizinlerinde tutar.

## Önemli Not

> **Uyarı:** Özel geliştirme kartınızın IO yapılandırması mevcut kartlardan farklıysa mevcut kart yapılandırmasının üzerine yazarak firmware derlemeyin. Yeni bir kart türü oluşturun veya `config.json` içindeki `builds` alanında farklı `name` ve `sdkconfig` makrolarıyla ayırın. Firmware paketlemek için `python scripts/release.py [kart-dizini]` komutunu kullanın.
>
> Mevcut yapılandırmayı doğrudan değiştirirseniz, ileride OTA güncellemesi sırasında özel firmware standart kart firmware'i ile ezilebilir ve cihaz düzgün çalışmayabilir. Her kartın benzersiz bir kimliği ve firmware güncelleme kanalı olmalıdır.

## Dizin Yapısı

Her geliştirme kartı dizini genellikle şu dosyaları içerir:

- `xxx_board.cc` - Kart düzeyi başlatma ve özellik kodu.
- `config.h` - Donanım pin eşlemesi ve kart yapılandırması.
- `config.json` - Hedef çip ve derleme seçenekleri.
- `README.md` - Karta özel açıklama dokümanı.

## Özel Kart Ekleme Adımları

### 1. Yeni kart dizini oluşturun

Önce `boards/` altında yeni bir dizin oluşturun. Adlandırma için `[marka]-[kart-türü]` biçimini kullanın; örnek: `m5stack-tab5`.

```bash
mkdir main/boards/my-custom-board
```

### 2. Yapılandırma dosyalarını oluşturun

#### `config.h`

`config.h` içinde tüm donanım yapılandırmasını tanımlayın:

- Ses örnekleme oranı ve I2S pinleri
- Ses codec adresi ve I2C pinleri
- Buton ve LED pinleri
- Ekran parametreleri ve pinleri

Örnek yapılandırma:

```c
#ifndef _BOARD_CONFIG_H_
#define _BOARD_CONFIG_H_

#include <driver/gpio.h>

// Ses yapılandırması
#define AUDIO_INPUT_SAMPLE_RATE  24000
#define AUDIO_OUTPUT_SAMPLE_RATE 24000

#define AUDIO_I2S_GPIO_MCLK GPIO_NUM_10
#define AUDIO_I2S_GPIO_WS   GPIO_NUM_12
#define AUDIO_I2S_GPIO_BCLK GPIO_NUM_8
#define AUDIO_I2S_GPIO_DIN  GPIO_NUM_7
#define AUDIO_I2S_GPIO_DOUT GPIO_NUM_11

#define AUDIO_CODEC_PA_PIN       GPIO_NUM_13
#define AUDIO_CODEC_I2C_SDA_PIN  GPIO_NUM_0
#define AUDIO_CODEC_I2C_SCL_PIN  GPIO_NUM_1
#define AUDIO_CODEC_ES8311_ADDR  ES8311_CODEC_DEFAULT_ADDR

// Buton yapılandırması
#define BOOT_BUTTON_GPIO        GPIO_NUM_9

// Ekran yapılandırması
#define DISPLAY_SPI_SCK_PIN     GPIO_NUM_3
#define DISPLAY_SPI_MOSI_PIN    GPIO_NUM_5
#define DISPLAY_DC_PIN          GPIO_NUM_6
#define DISPLAY_SPI_CS_PIN      GPIO_NUM_4

#define DISPLAY_WIDTH   320
#define DISPLAY_HEIGHT  240
#define DISPLAY_MIRROR_X true
#define DISPLAY_MIRROR_Y false
#define DISPLAY_SWAP_XY true

#define DISPLAY_OFFSET_X  0
#define DISPLAY_OFFSET_Y  0

#define DISPLAY_BACKLIGHT_PIN GPIO_NUM_2
#define DISPLAY_BACKLIGHT_OUTPUT_INVERT true

#endif // _BOARD_CONFIG_H_
```

#### `config.json`

`config.json`, `scripts/release.py` betiğinin otomatik derleme için kullandığı hedef çip ve derleme yapılandırmasını tanımlar:

```json
{
    "target": "esp32s3",
    "builds": [
        {
            "name": "my-custom-board",
            "sdkconfig_append": [
                "CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y",
                "CONFIG_PARTITION_TABLE_CUSTOM_FILENAME=\"partitions/v2/8m.csv\""
            ]
        }
    ]
}
```

Alan açıklamaları:

- `target`: Hedef çip modeli. Donanımla uyumlu olmalıdır; örnekler: `esp32`, `esp32s3`, `esp32c3`, `esp32c6`, `esp32p4`.
- `name`: Derleme çıktısı firmware paketinin adı. Genellikle dizin adıyla aynı tutulur.
- `sdkconfig_append`: Varsayılan yapılandırmaya eklenecek ek `sdkconfig` seçenekleri.

Yaygın `sdkconfig_append` örnekleri:

```json
"CONFIG_ESPTOOLPY_FLASHSIZE_4MB=y"
"CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y"
"CONFIG_ESPTOOLPY_FLASHSIZE_16MB=y"

"CONFIG_PARTITION_TABLE_CUSTOM_FILENAME=\"partitions/v2/4m.csv\""
"CONFIG_PARTITION_TABLE_CUSTOM_FILENAME=\"partitions/v2/8m.csv\""
"CONFIG_PARTITION_TABLE_CUSTOM_FILENAME=\"partitions/v2/16m.csv\""

"CONFIG_LANGUAGE_EN_US=y"
"CONFIG_LANGUAGE_ZH_CN=y"

"CONFIG_USE_DEVICE_AEC=y"
"CONFIG_WAKE_WORD_DISABLED=y"
```

### 3. Kart düzeyi başlatma kodunu yazın

`my_custom_board.cc` dosyasını oluşturun ve geliştirme kartının tüm başlatma mantığını burada uygulayın.

Temel bir kart sınıfında genellikle şu bölümler bulunur:

1. **Sınıf tanımı:** `WifiBoard` veya `Ml307Board` sınıfından türetilir.
2. **Başlatma fonksiyonları:** I2C, SPI, ekran, buton, ses codec ve benzeri bileşenleri hazırlar.
3. **Sanal fonksiyonlar:** `GetAudioCodec()`, `GetDisplay()`, `GetBacklight()` gibi fonksiyonları override eder.
4. **Kart kaydı:** `DECLARE_BOARD` makrosu ile kartı sisteme kaydeder.

```cpp
#include "wifi_board.h"
#include "codecs/es8311_audio_codec.h"
#include "display/lcd_display.h"
#include "application.h"
#include "button.h"
#include "config.h"
#include "mcp_server.h"

#include <esp_log.h>
#include <driver/i2c_master.h>
#include <driver/spi_common.h>

#define TAG "MyCustomBoard"

class MyCustomBoard : public WifiBoard {
private:
    i2c_master_bus_handle_t codec_i2c_bus_;
    Button boot_button_;
    LcdDisplay* display_;

    // I2C başlatma
    void InitializeI2c() {
        i2c_master_bus_config_t i2c_bus_cfg = {
            .i2c_port = I2C_NUM_0,
            .sda_io_num = AUDIO_CODEC_I2C_SDA_PIN,
            .scl_io_num = AUDIO_CODEC_I2C_SCL_PIN,
            .clk_source = I2C_CLK_SRC_DEFAULT,
            .glitch_ignore_cnt = 7,
            .intr_priority = 0,
            .trans_queue_depth = 0,
            .flags = {
                .enable_internal_pullup = 1,
            },
        };
        ESP_ERROR_CHECK(i2c_new_master_bus(&i2c_bus_cfg, &codec_i2c_bus_));
    }

    // Ekran için SPI başlatma
    void InitializeSpi() {
        spi_bus_config_t buscfg = {};
        buscfg.mosi_io_num = DISPLAY_SPI_MOSI_PIN;
        buscfg.miso_io_num = GPIO_NUM_NC;
        buscfg.sclk_io_num = DISPLAY_SPI_SCK_PIN;
        buscfg.quadwp_io_num = GPIO_NUM_NC;
        buscfg.quadhd_io_num = GPIO_NUM_NC;
        buscfg.max_transfer_sz = DISPLAY_WIDTH * DISPLAY_HEIGHT * sizeof(uint16_t);
        ESP_ERROR_CHECK(spi_bus_initialize(SPI2_HOST, &buscfg, SPI_DMA_CH_AUTO));
    }

    // Buton başlatma
    void InitializeButtons() {
        boot_button_.OnClick([this]() {
            auto& app = Application::GetInstance();
            if (app.GetDeviceState() == kDeviceStateStarting) {
                EnterWifiConfigMode();
                return;
            }
            app.ToggleChatState();
        });
    }

    // Ekran başlatma, ST7789 örneği
    void InitializeDisplay() {
        esp_lcd_panel_io_handle_t panel_io = nullptr;
        esp_lcd_panel_handle_t panel = nullptr;

        esp_lcd_panel_io_spi_config_t io_config = {};
        io_config.cs_gpio_num = DISPLAY_SPI_CS_PIN;
        io_config.dc_gpio_num = DISPLAY_DC_PIN;
        io_config.spi_mode = 2;
        io_config.pclk_hz = 80 * 1000 * 1000;
        io_config.trans_queue_depth = 10;
        io_config.lcd_cmd_bits = 8;
        io_config.lcd_param_bits = 8;
        ESP_ERROR_CHECK(esp_lcd_new_panel_io_spi(SPI2_HOST, &io_config, &panel_io));

        esp_lcd_panel_dev_config_t panel_config = {};
        panel_config.reset_gpio_num = GPIO_NUM_NC;
        panel_config.rgb_ele_order = LCD_RGB_ELEMENT_ORDER_RGB;
        panel_config.bits_per_pixel = 16;
        ESP_ERROR_CHECK(esp_lcd_new_panel_st7789(panel_io, &panel_config, &panel));

        esp_lcd_panel_reset(panel);
        esp_lcd_panel_init(panel);
        esp_lcd_panel_invert_color(panel, true);
        esp_lcd_panel_swap_xy(panel, DISPLAY_SWAP_XY);
        esp_lcd_panel_mirror(panel, DISPLAY_MIRROR_X, DISPLAY_MIRROR_Y);

        // Ekran nesnesini oluştur
        display_ = new SpiLcdDisplay(panel_io, panel,
                                    DISPLAY_WIDTH, DISPLAY_HEIGHT,
                                    DISPLAY_OFFSET_X, DISPLAY_OFFSET_Y,
                                    DISPLAY_MIRROR_X, DISPLAY_MIRROR_Y, DISPLAY_SWAP_XY);
    }

    // MCP araçlarını başlatma
    void InitializeTools() {
        // Ayrıntılar için MCP dokümanlarına bakın.
    }

public:
    MyCustomBoard() : boot_button_(BOOT_BUTTON_GPIO) {
        InitializeI2c();
        InitializeSpi();
        InitializeDisplay();
        InitializeButtons();
        InitializeTools();
        GetBacklight()->SetBrightness(100);
    }

    // Ses codec nesnesini döndür
    virtual AudioCodec* GetAudioCodec() override {
        static Es8311AudioCodec audio_codec(
            codec_i2c_bus_,
            I2C_NUM_0,
            AUDIO_INPUT_SAMPLE_RATE,
            AUDIO_OUTPUT_SAMPLE_RATE,
            AUDIO_I2S_GPIO_MCLK,
            AUDIO_I2S_GPIO_BCLK,
            AUDIO_I2S_GPIO_WS,
            AUDIO_I2S_GPIO_DOUT,
            AUDIO_I2S_GPIO_DIN,
            AUDIO_CODEC_PA_PIN,
            AUDIO_CODEC_ES8311_ADDR);
        return &audio_codec;
    }

    // Ekran nesnesini döndür
    virtual Display* GetDisplay() override {
        return display_;
    }

    // Arka ışık kontrolünü döndür
    virtual Backlight* GetBacklight() override {
        static PwmBacklight backlight(DISPLAY_BACKLIGHT_PIN, DISPLAY_BACKLIGHT_OUTPUT_INVERT);
        return &backlight;
    }
};

// Geliştirme kartını kaydet
DECLARE_BOARD(MyCustomBoard);
```

### 4. Derleme sistemi yapılandırmasını ekleyin

#### `Kconfig.projbuild` içine kart seçeneği ekleyin

`main/Kconfig.projbuild` dosyasında `choice BOARD_TYPE` bölümüne yeni kart seçeneğini ekleyin:

```kconfig
choice BOARD_TYPE
    prompt "Board Type"
    default BOARD_TYPE_BREAD_COMPACT_WIFI
    help
        Kart türü.

    # ... diğer kart seçenekleri ...

    config BOARD_TYPE_MY_CUSTOM_BOARD
        bool "My Custom Board"
        depends on IDF_TARGET_ESP32S3
endchoice
```

Notlar:

- `BOARD_TYPE_MY_CUSTOM_BOARD` yapılandırma adı büyük harfli olmalı ve alt çizgi kullanmalıdır.
- `depends on` hedef çipi belirtir; örnek: `IDF_TARGET_ESP32S3`, `IDF_TARGET_ESP32C3`.
- Menü açıklaması kullanıcıya gösterileceği için doğal ve kısa tutulmalıdır.

#### `CMakeLists.txt` içine kart yapılandırması ekleyin

`main/CMakeLists.txt` içinde kart türü seçim bloğuna yeni yapılandırmayı ekleyin:

```cmake
# elseif zincirine özel kart yapılandırmanızı ekleyin
elseif(CONFIG_BOARD_TYPE_MY_CUSTOM_BOARD)
    set(BOARD_TYPE "my-custom-board")  # Dizin adıyla aynı tutulur
    set(BUILTIN_TEXT_FONT font_puhui_basic_20_4)
    set(BUILTIN_ICON_FONT font_awesome_20_4)
    set(DEFAULT_EMOJI_COLLECTION twemoji_64)
endif()
```

Font ve ifade koleksiyonu seçiminde ekran çözünürlüğünü dikkate alın:

- Küçük ekranlar, 128x64 OLED: `font_puhui_basic_14_1` / `font_awesome_14_1`
- Orta küçük ekranlar, 240x240: `font_puhui_basic_16_4` / `font_awesome_16_4`
- Orta ekranlar, 240x320: `font_puhui_basic_20_4` / `font_awesome_20_4`
- Büyük ekranlar, 480x320 ve üzeri: `font_puhui_basic_30_4` / `font_awesome_30_4`

İfade koleksiyonu seçenekleri:

- `twemoji_32` - 32x32 piksel ifadeler, küçük ekranlar için.
- `twemoji_64` - 64x64 piksel ifadeler, büyük ekranlar için.

### 5. Yapılandırın ve derleyin

#### Yöntem 1: `idf.py` ile manuel yapılandırma

1. Hedef çipi ayarlayın:

   ```bash
   idf.py set-target esp32s3
   ```

2. Eski yapılandırmayı temizleyin:

   ```bash
   idf.py fullclean
   ```

3. Menü yapılandırmasını açın:

   ```bash
   idf.py menuconfig
   ```

   Menüde `VoiaX Asistan` -> `Kart Türü` yoluna gidin ve özel geliştirme kartınızı seçin.

4. Derleyin ve cihaza yazın:

   ```bash
   idf.py build
   idf.py flash monitor
   ```

#### Yöntem 2: `release.py` betiğini kullanın

Kart dizininde `config.json` varsa betik hedef çipi ve ek `sdkconfig` seçeneklerini otomatik uygular:

```bash
python scripts/release.py my-custom-board
```

Bu betik:

- `config.json` içindeki `target` değerini okuyarak hedef çipi ayarlar.
- `sdkconfig_append` seçeneklerini varsayılan yapılandırmaya ekler.
- Derlemeyi tamamlayıp firmware paketini üretir.

### 6. Kart README dosyasını yazın

Kart dizinindeki `README.md` içinde şu bilgileri belirtin:

- Kartın temel özellikleri
- Gerekli donanım ve bağlantılar
- Bilinen kısıtlar
- Derleme ve yazma komutları
- Özel `sdkconfig` gereksinimleri

## Yaygın Geliştirme Kartı Bileşenleri

### Ekran

Desteklenebilecek yaygın ekran sürücüleri:

- ST7789, SPI
- ILI9341, SPI
- SH8601, QSPI

### Ses codec

Yaygın codec ve ses bileşenleri:

- ES8311
- ES7210, mikrofon dizisi
- AW88298, güç amplifikatörü

### Güç yönetimi

Bazı geliştirme kartları güç yönetim çipi kullanır. Örnek: AXP2101. Kart başlatma kodunda pil, şarj ve güç durumu okuma akışlarını buna göre ekleyin.

### MCP cihaz kontrolü

MCP araçları ekleyerek asistanın cihaz özelliklerini çağırmasını sağlayabilirsiniz:

- Speaker: hoparlör kontrolü
- Screen: ekran parlaklığı kontrolü
- Battery: pil seviyesi okuma
- Light: ışık kontrolü

## Kart Sınıfı Kalıtım Yapısı

- `Board` - Temel kart sınıfı.
- `WifiBoard` - Wi-Fi bağlantılı kartlar.
- `Ml307Board` - 4G modüllü kartlar.
- `DualNetworkBoard` - Wi-Fi ve 4G arasında geçiş yapabilen kartlar.

## Geliştirme İpuçları

1. **Benzer kartları inceleyin:** Yeni kartınız mevcut bir karta benziyorsa, önce o kartın başlatma kodunu referans alın.
2. **Aşamalı ilerleyin:** Önce ekran gibi temel parçaları çalıştırın, ardından ses ve MCP araçları gibi daha karmaşık bölümleri ekleyin.
3. **Pin eşlemesini doğrulayın:** `config.h` içindeki tüm pinlerin donanımla uyumlu olduğundan emin olun.
4. **Donanım uyumluluğunu kontrol edin:** Codec, ekran sürücüsü, güç yönetimi ve çip hedefinin uyumunu doğrulayın.

## Olası Sorunlar

1. **Ekran doğru çalışmıyor:** SPI yapılandırmasını, mirror ayarlarını ve renk tersleme ayarını kontrol edin.
2. **Ses çıkışı yok:** I2S yapılandırmasını, PA enable pinini ve codec adresini kontrol edin.
3. **Ağa bağlanılamıyor:** Wi-Fi bilgilerini ve ağ yapılandırmasını kontrol edin.
4. **Sunucuyla iletişim kurulamıyor:** MQTT veya WebSocket yapılandırmasını kontrol edin.

## Referanslar

- ESP-IDF dokümantasyonu: https://docs.espressif.com/projects/esp-idf/
- LVGL dokümantasyonu: https://docs.lvgl.io/
- ESP-SR dokümantasyonu: https://github.com/espressif/esp-sr
