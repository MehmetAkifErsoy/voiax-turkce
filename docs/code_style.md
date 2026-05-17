# Kod Stili Kılavuzu

## Kod Formatlama Aracı

Bu projede kod stilini tutarlı tutmak için `clang-format` kullanılır. Proje kök dizininde Google C++ stil kılavuzu temel alınarak özelleştirilmiş bir `.clang-format` yapılandırması bulunur.

### `clang-format` Kurulumu

Kullanmadan önce `clang-format` aracının kurulu olduğundan emin olun:

- **Windows**:
  ```powershell
  winget install LLVM
  # 或者使用 Chocolatey
  choco install llvm
  ```

- **Linux**:
  ```bash
  sudo apt install clang-format  # Ubuntu/Debian
  sudo dnf install clang-tools-extra  # Fedora
  ```

- **macOS**:
  ```bash
  brew install clang-format
  ```

### Kullanım

1. **Tek dosyayı formatlama**:
   ```bash
   clang-format -i path/to/your/file.cpp
   ```

2. **Tüm projeyi formatlama**:
   ```bash
   # 在项目根目录下执行
   find main -iname *.h -o -iname *.cc | xargs clang-format -i
   ```

3. **Commit öncesi format kontrolü**:
   ```bash
   # 检查文件格式是否符合规范（不修改文件）
   clang-format --dry-run -Werror path/to/your/file.cpp
   ```

### IDE Entegrasyonu

- **Visual Studio Code**:
  1. C/C++ eklentisini kurun.
  2. Ayarlarda `C_Cpp.formatting` değerini `clang-format` olarak ayarlayın.
  3. İsterseniz kaydederken otomatik formatlamayı etkinleştirin: `editor.formatOnSave: true`.

- **CLion**:
  1. Ayarlarda `Editor > Code Style > C/C++` bölümünü açın.
  2. `Formatter` değerini `clang-format` olarak ayarlayın.
  3. Projedeki `.clang-format` yapılandırma dosyasını kullanın.

### Temel Format Kuralları

- Girinti 4 boşluk olmalıdır.
- Satır uzunluğu sınırı 100 karakterdir.
- Süslü parantezler Attach stilinde, kontrol ifadesiyle aynı satırda kullanılır.
- Pointer ve referans sembolleri sola hizalanır.
- Header include satırları otomatik sıralanır.
- Sınıf erişim belirteçleri -4 boşluk girinti kullanır.

### Notlar

1. Commit öncesinde kodun formatlandığından emin olun.
2. Formatlanmış kod hizalamasını elle değiştirmeyin.
3. Belirli bir kod bloğunun formatlanmasını istemiyorsanız aşağıdaki yorumlarla çevreleyin:
   ```cpp
   // clang-format off
   // 你的代码
   // clang-format on
   ```

### Sık Karşılaşılan Sorunlar

1. **Formatlama başarısız oluyor**:
   - `clang-format` sürümünün çok eski olmadığını kontrol edin.
   - Dosya kodlamasının UTF-8 olduğunu doğrulayın.
   - `.clang-format` dosyasının sözdizimini kontrol edin.

2. **Format beklenen gibi değil**:
   - Proje kök dizinindeki `.clang-format` yapılandırmasının kullanıldığını kontrol edin.
   - Başka bir konumdaki `.clang-format` dosyasının öncelikli olarak kullanılmadığını doğrulayın.

Sorun veya öneriler için issue ya da pull request açabilirsiniz.
