# BluFi Wi-Fi Kurulumu (esp-wifi-connect Entegrasyonu)

# Ön Bilgi

Bu doküman, VoiaX firmware içinde BluFi (BLE Wi-Fi kurulumu) özelliğinin nasıl etkinleştirileceğini ve proje içindeki `esp-wifi-connect` bileşeniyle Wi-Fi bağlantısının nasıl saklanacağını açıklar. Resmi BluFi protokol ayrıntıları için [Espressif dokümantasyonuna](https://docs.espressif.com/projects/esp-idf/zh_CN/stable/esp32/api-guides/ble/blufi.html) bakın.

## Gereksinimler

- BLE destekleyen bir çip ve uygun firmware yapılandırması gerekir.
- `idf.py menuconfig` içinde `WiFi Configuration Method -> Esp Blufi` seçeneğini etkinleştirin (`CONFIG_USE_ESP_BLUFI_WIFI_PROVISIONING=y`). BluFi kullanacaksanız aynı menüdeki Hotspot seçeneğini kapatın; aksi halde varsayılan olarak Hotspot kurulumu kullanılır.
- Varsayılan NVS ve event loop başlatma akışını koruyun; proje içindeki `app_main` bunu zaten yapar.
- `CONFIG_BT_BLUEDROID_ENABLED` ve `CONFIG_BT_NIMBLE_ENABLED` seçeneklerinden yalnızca biri etkin olmalıdır.

## Çalışma Akışı

1. Telefon, BluFi üzerinden cihaza bağlanır ve Wi-Fi SSID/parola bilgisini gönderir. Telefon, cihazın taradığı Wi-Fi listesini BluFi protokolüyle alabilir.
2. Cihaz, `ESP_BLUFI_EVENT_REQ_CONNECT_TO_AP` olayında bilgileri `SsidManager` içine yazar. Bu bilgiler `esp-wifi-connect` bileşeni tarafından NVS içinde saklanır.
3. Ardından `WifiStation` tarama ve bağlantı işlemini başlatır; durum BluFi üzerinden geri bildirilir.
4. Kurulum başarılıysa cihaz yeni Wi-Fi ağına otomatik bağlanır; başarısızsa hata durumu döner.

## Kullanım

1. `menuconfig` içinde `Esp Blufi` seçeneğini açın, firmware’i derleyip yükleyin.
2. Cihaz ilk kez başlatıldığında ve kayıtlı Wi-Fi yoksa otomatik olarak kurulum moduna girer.
3. EspBlufi App veya başka bir BluFi istemcisiyle cihazı bulun, bağlanın, gerekiyorsa şifreleme seçin, Wi-Fi SSID/parola bilgisini gönderin.
4. Sonucu kontrol edin:
   - Başarılı: BluFi bağlantının başarılı olduğunu bildirir ve cihaz Wi-Fi ağına bağlanır.
   - Başarısız: BluFi hata durumu döndürür; bilgileri yeniden gönderin veya yönlendiriciyi kontrol edin.

## Notlar

- BluFi kurulumu Hotspot kurulumu ile aynı anda kullanılmamalıdır. `menuconfig` içinde yalnızca bir kurulum yöntemi bırakın.
- Çoklu testlerde eski yapılandırmanın karışmaması için `wifi` NVS alanındaki kayıtlı SSID bilgisini temizleyin veya üzerine yazın.
- Özel BluFi istemcisi kullanıyorsanız resmi protokol frame formatını izleyin.
- EspBlufi App indirme bağlantıları resmi Espressif dokümanlarında yer alır.
- IDF 5.5.2 ile BluFi arayüzü değiştiği için 5.5.2 derlemelerinde BLE adı `VoiaX-Blufi`, 5.5.1 sürümünde `BLUFI_DEVICE` olabilir.
