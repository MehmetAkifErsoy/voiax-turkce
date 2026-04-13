# VoiaX - Türkçe Sesli Asistan Çalışma Planı
**Tarih:** 13 Nisan 2026  
**Proje:** VoiaX firmware + VoiaX sunucu  
**Hedef:** İkisinin sorunsuz, eksiksiz ve Türkçe olarak çalışması  
**Kurumsal Ad:** **VoiaX** (tüm "xiaozhi", "小智", "小志", "XiaoZhi" referansları VoiaX olarak değiştirilecek)

---

## ⚠️ KURUMSAL KİMLİK KURALI (TÜM ADIMLARDA GEÇERLİ)

**"VoiaX" kurumsal addır. Projede xiaozhi/小智/小志 ile ilgili hiçbir şey kalmayacak.**

Değiştirilecek bağlamlar:
- **Kullanıcıya görünen metinler** → xiaozhi/小智/小志 → **VoiaX** (ZORUNLU)
- **Web panel arayüzü** → xiaozhi → **VoiaX** (ZORUNLU)  
- **Sistem promptları** → 小智/小志 karakteri → **VoiaX** Türk asistanı (ZORUNLU)
- **Hata mesajları** → "小智现在有点忙" → Türkçe VoiaX mesajı (ZORUNLU)
- **Docker container isimleri** → xiaozhi-esp32-server → voiax-server (İSTEĞE BAĞLI, çalışmayı etkilemez)
- **URL path'leri** → `/xiaozhi/v1/` → DOKUNULMAYACAK (firmware bağımlılığı var, değişirse bağlantı kopar)
- **Veritabanı adı** → `xiaozhi_esp32_server` → DOKUNULMAYACAK (veri kaybı riski)
- **Java package isimleri** → `xiaozhi.common.*` → DOKUNULMAYACAK (tüm import'ları kırar, risk çok yüksek)
- **Dockerfile path'leri** → `/opt/xiaozhi-esp32-server/` → DOKUNULMAYACAK (container iç yapısı)

### Tarama Sonucu: xiaozhi/小智 İçeren Dosyalar

**Sunucu (Python) - Kullanıcıya Görünen:**
| Dosya | Ne var | Ne yapılacak |
|-------|--------|-------------|
| `config.yaml` | 小智/小志 prompt, wakeup, error msg | ✅ VoiaX'a çevir |
| `connection.py` | TOOL_CALLING_RULES içinde | ✅ VoiaX'a çevir |
| `http_server.py` | Route path'leri | ⚠️ Path'lere dokunma (firmware bağımlı) |
| `ota_handler.py` | OTA route | ⚠️ Path'lere dokunma |
| `performance_tester_llm.py` | Test cümleleri | ✅ VoiaX'a çevir |
| `homeassistant.py` | Prompt içinde 小智 | ✅ VoiaX'a çevir |
| `powermem.py` | Memory prompt | ✅ VoiaX'a çevir |

**Web Panel (Vue.js) - Arayüz:**
| Dosya | Ne var | Ne yapılacak |
|-------|--------|-------------|
| `HeaderBar.vue` | Başlık "小智" | ✅ VoiaX'a çevir |
| `login.vue` | Hoşgeldin mesajı | ✅ VoiaX'a çevir |
| `register.vue` | Kayıt sayfası | ✅ VoiaX'a çevir |
| `retrievePassword.vue` | Şifre sıfırlama | ✅ VoiaX'a çevir |
| `roleConfig.vue` | Rol yapılandırma | ✅ VoiaX'a çevir |
| `TemplateQuickConfig.vue` | Şablon config | ✅ VoiaX'a çevir |
| `ChatHistoryDialog.vue` | Sohbet geçmişi | ✅ VoiaX'a çevir |
| `FunctionDialog.vue` | Fonksiyon dialog | ✅ VoiaX'a çevir |
| `package.json` | Proje adı | ✅ VoiaX'a çevir |
| `i18n/*.js` (de, pt_BR, vi, zh_TW) | Diğer dillerde xiaozhi | ✅ VoiaX'a çevir |
| `public/*.html` | Privacy policy, offline | ✅ VoiaX'a çevir |

**Docker/Altyapı - İsteğe Bağlı:**
| Dosya | Ne var | Ne yapılacak |
|-------|--------|-------------|
| `docker-compose_all.yml` | Container isimleri | ⚠️ İsteğe bağlı |
| `docker-compose.yml` | Container isimleri | ⚠️ İsteğe bağlı |
| `Dockerfile-*` | Path, image isimleri | ⚠️ Dokunma |

---

## MEVCUT DURUM ANALİZİ

### Firmware (ESP32-S3) - `C:\Users\oxygen\Documents\vscode_projeler\xioazhi_test\`
- **Board:** bread-compact-wifi-lcd
- **Dil:** `CONFIG_LANGUAGE_TR_TR=y` ✅ (Türkçe UI ayarlanmış)
- **OTA URL:** `http://104.238.21.24:8003/xiaozhi/ota/`
- **WebSocket:** OTA'dan dinamik alınıyor (NVS'ye kaydedilir)
- **Ses:** Opus codec, 24000 Hz sample rate

### Sunucu - `voiax-turkce-main/xiaozhi-esp32-server/`
- **Dil:** Tamamen Çince (config, prompt, wakeup words, pluginler)
- **Docker:** docker-compose_all.yml ile çalışıyor (server + web panel + MySQL + Redis)
- **Zaman dilimi:** Asia/Shanghai (Çin)
- **Web Panel:** manager-api (Java) + manager-web (Vue.js)

---

## ADIM ADIM ÇALIŞMA PLANI

### ADIM 1: docker-compose_all.yml Düzenleme
**Durum:** ✅ Tamamlandı  
**Dosya:** `main/xiaozhi-server/docker-compose_all.yml`

Yapılacaklar:
- [ ] `TZ=Asia/Shanghai` → `TZ=Europe/Istanbul` (tüm servisler)
- [ ] `PYTHONIOENCODING=utf-8` environment ekle (server container)
- [ ] Build context path'leri düzenle (yerel sunucu yapısına göre)
- [ ] MySQL `MYSQL_INITDB_ARGS` zaten utf8mb4 ✅

---

### ADIM 2: config.yaml Ana Yapılandırma
**Durum:** ✅ Tamamlandı  
**Dosya:** `main/xiaozhi-server/config.yaml`

Yapılacaklar:
- [ ] `server.websocket` → `ws://104.238.21.24:8000/xiaozhi/v1/`
- [ ] `server.vision_explain` → `http://104.238.21.24:8003/mcp/vision/explain`
- [ ] `server.timezone_offset` → `+3` (Türkiye UTC+3)
- [ ] `xiaozhi.audio_params.sample_rate` → `24000` (firmware ile eşleşmeli) ✅ Zaten doğru
- [ ] `exit_commands` → Türkçe: `["çıkış", "kapat", "görüşürüz", "hoşça kal"]`
- [ ] `wakeup_words` → Türkçe: `["merhaba voiax", "hey voiax", "voiax"]`
- [ ] `module_test.test_sentences` → Türkçe test cümleleri
- [ ] `mcp_endpoint` → gerekirse ayarla

---

### ADIM 3: Sistem Prompt (Karakter) Türkçeleştirme
**Durum:** ✅ Tamamlandı (ADIM 2 ile birlikte yapıldı)  
**Dosya:** `main/xiaozhi-server/config.yaml` (prompt bölümü)

Yapılacaklar:
- [ ] `prompt` alanını tamamen Türkçe VoiaX karakterine çevir:
  - Türk yapay zeka asistanı "VoiaX"
  - Samimi, yardımsever, Türkçe konuşan
  - Kullanıcıya "sen" diye hitap eden

---

### ADIM 4: agent-base-prompt.txt Şablon Türkçeleştirme
**Durum:** ✅ Tamamlandı  
**Dosya:** `main/xiaozhi-server/agent-base-prompt.txt`

Yapılacaklar:
- [ ] `<language>` bölümü: "Türkçe" → `{{language}}`  zaten template, TTS config'den alıyor
- [ ] `<emotion>` bölümü: Tüm Çince ifadeleri Türkçeye çevir
  - "哈哈、嘿嘿、噗" → "haha, hehe"
  - "不会吧？！" → "Yok artık?!", "İnanamıyorum!"
  - "别急嘛~" → "Sakin ol~", "Merak etme"
- [ ] `<communication_style>` bölümü: Türkçe doğal konuşma tarzı
  - Çince ünlemleri kaldır (呀、呢、啦)
  - Türkçe doğal konuşma tarzı yaz
- [ ] `<communication_length_constraint>` bölümü: Türkçeye çevir
- [ ] `<speaker_recognition>` bölümü: Türkçeye çevir
- [ ] `<tool_calling>` bölümü (connection.py içinde): Türkçeye çevir
- [ ] WEEKDAY_MAP (prompt_manager.py): Türkçe gün isimleri ekle

---

### ADIM 5: Web Panel (manager-web) Türkçe Dil Desteği
**Durum:** ✅ Tamamlandı  
**Dosyalar:** `main/manager-web/src/i18n/`

**Yapılanlar:**
- [x] `tr.js` dosyası oluşturuldu (~1350 satır, tam Türkçe çeviri)
- [x] `index.js`'e Türkçe dil kaydı eklendi (import, browser detection, messages)
- [x] `en.js`'e `language.tr: 'Türkçe'` eklendi
- **NOT:** en.js'deki bozuk key adları (Yapay Zeka Birimi, Hizmet Sağlayıcı, Kontrol Merkezi vb.) Vue bileşen bağımlılığı nedeniyle aynı bırakıldı. tr.js'de aynı key'ler kullanıldı.

**Çevrilecek ana bölümler (~1347 satır):**
| Bölüm | Satır Sayısı (yaklaşık) |
|-------|------------------------|
| Login/Register/Password | ~80 |
| Header/Navigation | ~20 |
| MCP Tool Call Dialog | ~90 |
| Dictionary/Parameter Dialogs | ~30 |
| Voice/Audio Dialogs | ~20 |
| Firmware Dialog | ~20 |
| Voice Print | ~30 |
| Device Management | ~60 |
| Chat History | ~15 |
| Role/Agent Config | ~100+ |
| Model Config | ~50+ |
| OTA Management | ~30 |
| User Management | ~20 |
| Common (buttons, messages) | ~50 |
| Diğerleri | ~700+ |

---

### ADIM 6: Plugin Açıklamalarını Türkçeleştirme
**Durum:** ✅ Tamamlandı  
**Dosyalar:** `main/xiaozhi-server/plugins_func/functions/` altındaki tüm dosyalar

Yapılacaklar:
- [ ] `handle_exit_intent.py`: description → Türkçe, varsayılan veda mesajı Türkçe
- [ ] `get_weather.py`: description → Türkçe, varsayılan konum → İstanbul veya kullanıcı şehri
- [ ] `get_time.py`: description → Türkçe
- [ ] `change_role.py`: description → Türkçe
- [ ] `play_music.py`: description → Türkçe
- [ ] `get_news_from_chinanews.py`: Çin haber kaynağı → devre dışı bırak veya Türk haber kaynağı ekle
- [ ] `get_news_from_newsnow.py`: Çin haber kaynağı → devre dışı bırak veya düzenle

---

### ADIM 7: Gemini LLM Provider Patch (Bilinen Bug Düzeltmeleri)
**Durum:** ✅ Tamamlandı  
**Dosya:** `main/xiaozhi-server/core/providers/llm/gemini/gemini.py`

Yapılacaklar:
- [ ] `_build_tools()` fonksiyonuna `_clean_schema()` ekle (minimum/maximum/default strip)
- [ ] `timeout=self.timeout` parametresini `generate_content()`'den kaldır

**NOT:** Bu patch'ler daha önce Docker içinde yapılmıştı ama kaynak kodda kalıcı değildi.

---

### ADIM 8: LLM Factory Patch (OpenAI Uyumluluğu)
**Durum:** ✅ Tamamlandı  
**Dosya:** `main/xiaozhi-server/core/utils/llm.py`

Yapılacaklar:
- [ ] `create_instance()` fonksiyonuna `LLM_OpenAI → openai` mapping ekle
  - Web panel "LLM_OpenAI" olarak kaydeder, ama dizin adı "openai"
  - Bu mapping olmadan Groq/OpenAI uyumlu LLM'ler çalışmaz

---

### ADIM 9: data/.config.yaml Oluşturma (Sunucu Çalışma Config)
**Durum:** ✅ Tamamlandı  
**Dosya:** `main/xiaozhi-server/data/.config.yaml` (oluşturulacak)

**Karar:** ✅ **Web Panel modu (B)** seçildi
- manager-api URL: `http://xiaozhi-esp32-server-web:8002/xiaozhi`
- manager-api secret: web panelden alınacak (server.secret)
- Sunucu IP/port: 0.0.0.0:8000
- prompt_template: agent-base-prompt.txt
- **NOT:** Web panel çalışıyor ama kaynak koddaki değişiklikler (prompt, plugin desc vb.) panelden bağımsız, doğrudan koda yazılacak

---

### ADIM 10: Prompt Manager Türkçe Desteği
**Durum:** ✅ Tamamlandı  
**Dosya:** `main/xiaozhi-server/core/utils/prompt_manager.py`

Yapılacaklar:
- [ ] `WEEKDAY_MAP` → Türkçe gün isimleri ekle:
  ```python
  "Monday": "Pazartesi",
  "Tuesday": "Salı",
  "Wednesday": "Çarşamba",
  "Thursday": "Perşembe",
  "Friday": "Cuma",
  "Saturday": "Cumartesi",
  "Sunday": "Pazar",
  ```
- [ ] `get_weather` fonksiyonundaki `lang` parametresi → `tr_TR`
- [ ] Hata mesajları (isteğe bağlı, çalışmayı etkilemez)

---

### ADIM 11: connection.py Tool Calling Rules Türkçeleştirme
**Durum:** ✅ Tamamlandı  
**Dosya:** `main/xiaozhi-server/core/connection.py`

Yapılacaklar:
- [ ] `TOOL_CALLING_RULES` string → Türkçeye çevir
- [ ] `exit_commands` → Türkçe (config.yaml'dan alır, ama kontrol et)
- [ ] `get_system_error_response` → Türkçe hata mesajları

---

### ADIM 12: TTS Dil Ayarı
**Durum:** ✅ Tamamlandı (ADIM 2 ile birlikte - EdgeTTS tr-TR-EmelNeural)  
**Config ayarı (config.yaml veya web panel)**

Yapılacaklar:
- [ ] Edge TTS provider: voice → `tr-TR-EmelNeural` (kadın) veya `tr-TR-AhmetNeural` (erkek)
- [ ] TTS config'e `language: "Türkçe"` ekle (prompt_manager bunu kullanır)
- [ ] `private_voice` ayarı → `tr-TR-EmelNeural`

---

### ADIM 13: ASR (Konuşma Tanıma) Ayarı  
**Durum:** ✅ Tamamlandı (ADIM 2 ile birlikte - GroqASR whisper-large-v3-turbo)  
**Config ayarı**

Yapılacaklar:
- [ ] Groq Whisper ASR: zaten çok dilli, Türkçe destekler ✅
- [ ] `base_url`: `https://api.groq.com/openai/v1/audio/transcriptions`
- [ ] `model_name`: `whisper-large-v3-turbo`

---

### ADIM 14: LLM (Dil Modeli) Ayarı
**Durum:** ✅ Tamamlandı (ADIM 2 ile birlikte - GroqLLM llama-3.3-70b-versatile)  
**Config ayarı**

Yapılacaklar:
- [ ] Groq LLM: `llama-3.3-70b-versatile`
- [ ] `base_url`: `https://api.groq.com/openai/v1`
- [ ] `api_key`: `gsk_eSK2NMi...KMnrFg` (mevcut ✅)
- [ ] Type: `openai` (OpenAI uyumlu API)

**⚠️ GÜVENLİK:** API key'i git'e push etme! `.config.yaml` veya `.env` dosyasında tut.

---

### ADIM 15: Docker Image Build & Deploy
**Durum:** ⬜ Bekliyor

Yapılacaklar:
- [ ] Tüm değişiklikleri commit et
- [ ] Düzenlenmiş kaynak kodu sunucuya (104.238.21.24) gönder
- [ ] Docker image'ları yeniden build et: `docker-compose -f docker-compose_all.yml build`
- [ ] Container'ları yeniden başlat: `docker-compose -f docker-compose_all.yml up -d`
- [ ] Logları kontrol et: `docker logs xiaozhi-esp32-server -f`

---

### ADIM 16: Test & Doğrulama
**Durum:** ⬜ Bekliyor

Yapılacaklar:
- [ ] Web panel erişimi: http://104.238.21.24:8002
- [ ] WebSocket bağlantısı: ws://104.238.21.24:8000/xiaozhi/v1/
- [ ] OTA endpoint: http://104.238.21.24:8003/xiaozhi/ota/
- [ ] Firmware flash et ve test et
- [ ] Türkçe konuşma tanıma (ASR) testi
- [ ] Türkçe yanıt üretme (LLM) testi
- [ ] Türkçe ses sentezi (TTS) testi
- [ ] Araç çağırma (hava durumu, çıkış) testi

---

## KARAR GEREKTİREN KONULAR (ÇÖZÜLDÜ)

1. **~~Standalone vs Web Panel modu?~~** → ✅ **Web Panel modu**
   - Web panel zaten çalışıyor (http://104.238.21.24:8002)
   - Kaynak kod değişiklikleri (prompt, plugin vb.) doğrudan dosyalara yazılacak
   - TTS/ASR/LLM model ayarları web panelden yönetilecek
   
2. **~~Haber eklentileri~~** → ✅ **Türk haber kaynağı eklenecek**

3. **~~Home Assistant~~** → ✅ **Evet, isteğe bağlı olarak kalacak**

4. **~~API Key'ler~~** → ✅ **Groq API key mevcut**

5. **~~Sunucuya dosya transferi~~** → ✅ **Git push**

---

## ÖNCELİK SIRASI

| Öncelik | Adım | Açıklama |
|---------|------|----------|
| 🔴 | 2,3,4 | config.yaml + prompt (temel çalışma) |
| 🔴 | 7,8 | LLM bug fix'leri (çalışma için kritik) |
| 🔴 | 9 | data/.config.yaml (sunucu başlatma) |
| 🟡 | 1 | docker-compose (zaman dilimi) |
| 🟡 | 5 | Web Panel Türkçe i18n (arayüz) |
| 🟡 | 6 | Plugin açıklamaları |
| 🟡 | 10,11 | Prompt manager + tool rules |
| 🟡 | 12,13,14 | TTS/ASR/LLM config |
| 🟢 | 15,16 | Build, deploy, test |

---

## NOTLAR

- Docker patch'leri kalıcı olması için kaynak kodda yapılmalı (container rebuild'de kaybolmaz)
- Firmware zaten Türkçe UI'ye ayarlanmış (CONFIG_LANGUAGE_TR_TR=y)
- Firmware OTA URL doğru: 104.238.21.24:8003
- Sample rate: Firmware 24000 Hz, sunucu config'de de 24000 Hz ✅
- Opus codec: Her iki tarafta da uyumlu ✅
