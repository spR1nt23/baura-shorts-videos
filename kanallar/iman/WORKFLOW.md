# KOMUTA Talimatı: İman Işığı Günlük YouTube Shorts Yüklemesi

*Hazırlayan: Claude, 13 Kasım 2026. Kaynak: s1 klasöründeki Excel'ler ve DEVAM_NOTU.txt.*

## 0. Önce şunu bil (13 Kasım itibarıyla durum)

- **1–45 yüklendi ve planlandı.** Son video 10 Kasım'da yayınlandı. Studio'da doğrulandı.
- **46–55 henüz yüklenmedi** (Excel'de "bekliyor"). Dosyaları `yuklenecek` klasöründe hazır.
- **Excel'deki 46 ve sonrası tarihler geçmişte kaldı.** Excel'de 46 → 12 Kasım 18:00 yazıyor ama bu saat geçti. İlk yüklemeden önce aşağıdaki **Bölüm 6 "Eski tarihler"** kuralını uygula.
- **12 Kasım'da yükleme yapılıp yapılmadığı kesin değil.** Excel'de kayıt yok. İlk çalıştırmada **Studio'da 46–55 başlıklarını ara** (Bölüm 8, adım 2). Varsa tekrar yükleme, Excel'i "yüklendi" yap.

## 1. Kanal ve hesap

| | |
|---|---|
| Kanal adı | **İman Işığıı** (Studio'da iki ı ile yazıyor) |
| Kanal kimliği | `UChkANcb8S13MGNOZNnSZnfw` |
| Studio | https://studio.youtube.com/channel/UChkANcb8S13MGNOZNnSZnfw |
| Shorts listesi | https://studio.youtube.com/channel/UChkANcb8S13MGNOZNnSZnfw/videos/short |
| Yükleme penceresi | https://studio.youtube.com/channel/UChkANcb8S13MGNOZNnSZnfw/videos/short?d=ud |
| Google hesabı | `berke.arica23@gmail.com` |

**Hesap uyarısı:** Chrome'da birden fazla Google hesabı açık (berkearica.00@gmail.com → Baura_shorts / Español en 7 dias, mehmetturan1990@gmail.com, selinarica.2007@gmail.com, sin_sonsuzluk@hotmail.com). Studio sık sık başka hesapla açılıyor ve **"Bu sayfayı görüntüleme izniniz yok"** hatası veriyor. Bu durumda:
YouTube → sağ üst avatar → **Hesap değiştir** → `berke.arica23@gmail.com` altında **İman Işığıı**'nı seç. Sonra Studio linkini yeniden aç.
Aynı hesapta bir de **Millioner_lifestyle** kanalı var. Ona **yükleme yapma.**

## 2. Klasörler ve dosyalar (tam yollar)

| Ne | Tam yol |
|---|---|
| Ana klasör | `C:\Users\user\OneDrive\Desktop\s1` |
| Yüklemeye hazır videolar | `C:\Users\user\OneDrive\Desktop\s1\yuklenecek` |
| Yüklenenlerin taşınacağı klasör | `C:\Users\user\OneDrive\Desktop\s1\yuklendi` (**yeni**, yoksa oluştur) |
| Ana takvim | `C:\Users\user\OneDrive\Desktop\s1\YouTube_Yayin_Takvimi.xlsx` |
| Özet liste | `C:\Users\user\OneDrive\Desktop\s1\Kalan_Yayin_Listesi.xlsx` |
| Devam notu | `C:\Users\user\OneDrive\Desktop\s1\DEVAM_NOTU.txt` |
| Kaynak zip'ler | `C:\Users\user\OneDrive\Desktop\s1\<konu klasörü>\<n>.zip` (bazıları doğrudan `C:\Users\user\OneDrive\Desktop\s1` altında) |

**Not:** `yuklenecek` içindeki `0001`–`0005` dosyaları eski. Zaten yüklendiler. **Onları yükleme.** İlk çalıştırmada `yuklendi` klasörüne taşı.

## 3. Dosya adı düzeni

`yuklenecek` içindeki dosyalar: **`NNNN_<Video dosyası>`**
- `NNNN` = Excel'deki **Sıra**, 4 haneli, başı sıfırla doldurulmuş (46 → `0046`)
- `<Video dosyası>` = Excel'in **I sütunu** (zip'in içindeki orijinal ad), örn. `vidN03_isra_110.mp4`
- Örnek: `0046_vidN03_isra_110.mp4`

**`yuklenecek`'te dosya yoksa (56 ve sonrası şu an yok):**
1. Excel **H sütunu (Kaynak zip)** yolunu `C:\Users\user\OneDrive\Desktop\s1\` ile birleştir. Örn. `borç ödeme  7.zip` → `C:\Users\user\OneDrive\Desktop\s1\borç ödeme  7.zip`. Dikkat: "borç ödeme" ile "7" arasında **iki boşluk** var.
2. Zip'in içinden **I sütunundaki** dosyayı çıkar.
3. `NNNN_` önekiyle `yuklenecek`'e koy.
4. Bazı satırlarda kaynak zip değil doğrudan mp4 (örn. `dehşet korku azap/31.mp4`, sıra 204). O zaman dosyayı kopyalaman yeterli.

Kontrol edildi: `borç ödeme  7.zip` içinde vidB01–vidB10 var (sıra 51–60). `Allahın hakkı ile korkup gazabından 3\7.zip` içinde vidF17–vidF21 var (sıra 61–65).

## 4. Excel yapısı

### YouTube_Yayin_Takvimi.xlsx (ana kaynak, buna göre çalış)
Sayfa **"Takvim"**. 1. satır başlık, 2–1242 arası 1.241 video.

| Sütun | Başlık | Ne işe yarar |
|---|---|---|
| A | Sıra | Video numarası. **Bazı hücreler sayı, bazıları metin** ("44"). Karşılaştırırken sayıya çevir. |
| B | Tarih | `YYYY-MM-DD` metni (örn. `2026-11-12`) |
| C | Saat | `HH:MM` metni |
| D | Konu | **Oynatma listesi adı** |
| E | Başlık | YouTube başlığı (olduğu gibi) |
| F | Açıklama | YouTube açıklaması (olduğu gibi, ~2.200 karakter) |
| G | Etiketler | Virgülle ayrılmış 9 etiket |
| H | Kaynak zip | `s1`'e göre göreli yol |
| I | Video dosyası | Zip içindeki mp4 adı |
| J | Durum | `bekliyor` / `yüklendi` (ayrıca `yayınlandı` da sayılıyor) |

Diğer sayfalar:
- **"Özet"**: Sayımlar formülle hesaplanıyor. Oradaki "Günlük video" satırındaki saatler **eski**, dikkate alma.
- **"Atlanan kopyalar"**: Birebir aynı olduğu için takvime alınmayan 53 video. **Bunları yükleme.**

### Kalan_Yayin_Listesi.xlsx (özet, okunabilir liste)
- **"Yayın Listesi"** sayfası. Sütunlar: Gün, Tarih (örn. `13 Kasım 2026`), Saat, Sıra, Konu (oynatma listesi), Sure / Ayet, Başlık, Video dosyası.
  - **Gün** ve **Tarih** sadece her günün ilk satırında dolu, diğer 4 satırda boş.
- **"Özet"** sayfası: Kalan video, Başlangıç, Bitiş, Günlük saatler.
- Bu dosyada Durum sütunu yok. Bilgi için var, **asıl kaynak Takvim**.

## 5. Sıradaki videoyu bulma ve yüklenenleri işaretleme

1. Takvim'de **Durum (J) = `bekliyor`** olan satırlardan **Sıra (A) en küçük** olanı al. Sıradaki budur. Bugün itibarıyla bu **46**.
2. Günde 5 video: Sıradaki 5 `bekliyor` satırı o günün 5 saatine gider.
3. Bir video **Studio'da "Planlandı" olarak kaydedildikten sonra**:
   - Takvim'de o satırın **J sütununu `yüklendi`** yap.
   - Gerçek yayın tarihi/saati Excel'dekinden farklıysa **B ve C'yi de** gerçekte kullanılanla güncelle.
   - Dosyayı `yuklenecek` → `yuklendi` klasörüne **taşı**.
4. Günün partisi bitince:
   - Kalan_Yayin_Listesi.xlsx'i tutarlı tut (tarihler değiştiyse güncelle).
   - DEVAM_NOTU.txt'nin sonuna kısa bir satır ekle, örn. `13 Kasım: 46–50 yüklendi, 14 Kasım 18:00–21:00. Sıradaki: 51.`
5. Excel'i kaydetmeden önce dosyanın açık olmadığından emin ol. OneDrive klasöründe olduğu için kilitlenebilir.

## 6. Yayın saatleri

- **Sadece şu 5 saat, İstanbul saati (GMT+3):** **18:00, 18:30, 19:00, 20:00, 21:00**. Günde 5 video, başka saat yok.
- Studio'da planlarken saat dilimi **Türkiye (GMT+03:00)** olmalı.
- **Eski tarihler kuralı:** Bir `bekliyor` satırının tarih/saati geçmişteyse ya da şu andan **en az 1 saat** sonrasında değilse:
  - O satırı ve sonraki **bütün** `bekliyor` satırlarını, sırayı bozmadan, **bir sonraki uygun slottan** başlayarak 5 saate yeniden dağıt.
  - Hem Takvim'in B/C sütunlarını hem Kalan_Yayin_Listesi.xlsx'i güncelle.
  - Atlanan saat olmasın, aynı saate iki video düşmesin.
- **Günlük sınır:** Kanal doğrulanmadığı için YouTube günde **yaklaşık 10 video** yüklemeye izin veriyor. Bir çalıştırmada en fazla 10 yükle. Sınır hatası gelirse dur, ertesi gün devam et.

## 7. Video ayarları (her video için)

| Alan | Değer |
|---|---|
| **Başlık** | Takvim **E** sütunu, harfi harfine. Şablon: `<Konu> \| <Sure> <Ayet> #shorts`. 100 karakteri geçmez. |
| **Açıklama** | Takvim **F** sütunu, **olduğu gibi**. Kısaltma ya da düzenleme yapma. |
| **Etiketler** | Takvim **G** sütunu (9 etiket, virgülle). Studio'da "Daha fazla göster" → Etiketler. |
| **Kitle** | **"Hayır, çocuklara özel değil"** |
| **Oynatma listesi** | Takvim **D** sütunundaki konu adı (bkz. Bölüm 7.1) |
| **Görünürlük** | **Planla** → Excel'deki tarih + saat (Bölüm 6), Türkiye saati |
| Diğer | Varsayılan bırak |

**Açıklamanın yapısı** (kontrol için, F sütununda zaten hazır):
1. Konu adı
2. `<Sure> Suresi <ayet>. ayet(ler)`
3. "Bu videoda … Arapça aslı, okunuşu ve Türkçe mealiyle yer alıyor."
4. Abonelik cümlesi
5. Sabit metin: "Bütün Dünya Size Verilmiş Olabilir mi? (Tirmizî, Zühd,34)" yazısı
6. Sabit metin: "Açıklama:" ve Tevbe 129 bölümü
7. **21 hashtag**:
   - Videoya özel 6 tane: `#dua #kuran #ayet #<sure>suresi #<konu> #shorts`
   - Sabit 15 tane: `#allah #islam #keşfet #namaz #kuranıkerim #kuranıkerimmeali #ayetler #dualar #duakabulolsun #amin #hadisler #tevekkül #şükür #iman #maneviyat`

**Etiket yapısı:** `dua, kuran, ayet, kuran ayetleri, dualar, <Sure> suresi, <Konu>, islam, shorts`

### 7.1 Oynatma listesi kuralı
- Liste adı = Takvim **D** sütunu (örn. `Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ)`, `Borçtan Kurtulma Duası`).
- Liste yoksa oluştur. Görünürlük herkese açık. Sıralama **"Yayınlandığı tarih (en eski)"**.
- **Sıra 51'den itibaren yeni liste: "Borçtan Kurtulma Duası".** Büyük ihtimalle henüz yok, oluşturulması gerekecek.
- Bir videoyu yalnızca kendi konusunun listesine ekle.

## 8. Günlük akış (özet)

1. Studio'yu aç. Doğru kanal mı (**İman Işığıı**) kontrol et, değilse Bölüm 1'deki gibi hesap değiştir.
2. Shorts listesinde sıradaki videoların başlıklarını ara. **Zaten varsa yükleme.** Excel'i `yüklendi` yap, dosyayı taşı.
3. Takvim'den sıradaki 5 `bekliyor` satırını al (Bölüm 5). Tarihleri kontrol et (Bölüm 6).
4. Her biri için: dosyayı `yuklenecek`'ten (yoksa zip'ten, Bölüm 3) yükle. Bölüm 7'deki ayarları gir. **Planla.**
5. Her video sonrası Excel'i işaretle ve dosyayı `yuklendi`'ye taşı (Bölüm 5).
6. Bitince DEVAM_NOTU.txt'ye bir satır ekle.
7. Hata, sınır uyarısı, telif/kısıtlama bildirimi ya da beklenmedik bir şey olursa dur ve kullanıcıya bildir.

## 9. Sıradaki ilk 5 video (Excel'den, 13 Kasım itibarıyla)

### Sıra 46
- **Dosya:** `C:\Users\user\OneDrive\Desktop\s1\yuklenecek\0046_vidN03_isra_110.mp4`
- **Excel'deki plan:** 2026-11-11 18:00 (geçmişte kaldı, aşağıdaki "Eski tarihler" kuralına bak)
- **Başlık:** `Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ) | İsrâ 110 #shorts`
- **Oynatma listesi:** Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ)
- **Etiketler:** `dua,kuran,ayet,kuran ayetleri,dualar,İsrâ suresi,Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ),islam,shorts`
- **Kaynak zip:** `C:\Users\user\OneDrive\Desktop\s1\Allahın 99 ismi 6.zip` → içindeki `vidN03_isra_110.mp4`
- **Açıklama:** Excel'deki F sütununun tamamı (2197 karakter). İlk satırları:
```
Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ)
İsrâ Suresi 110. ayet
```

### Sıra 47
- **Dosya:** `C:\Users\user\OneDrive\Desktop\s1\yuklenecek\0047_vidN04_taha_5_8.mp4`
- **Excel'deki plan:** 2026-11-11 18:30 (geçmişte kaldı, aşağıdaki "Eski tarihler" kuralına bak)
- **Başlık:** `Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ) | Tâhâ 5-8 #shorts`
- **Oynatma listesi:** Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ)
- **Etiketler:** `dua,kuran,ayet,kuran ayetleri,dualar,Tâhâ suresi,Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ),islam,shorts`
- **Kaynak zip:** `C:\Users\user\OneDrive\Desktop\s1\Allahın 99 ismi 6.zip` → içindeki `vidN04_taha_5_8.mp4`
- **Açıklama:** Excel'deki F sütununun tamamı (2203 karakter). İlk satırları:
```
Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ)
Tâhâ Suresi 5-8. ayetler
```

### Sıra 48
- **Dosya:** `C:\Users\user\OneDrive\Desktop\s1\yuklenecek\0048_vidN05_hadid_1_3.mp4`
- **Excel'deki plan:** 2026-11-11 19:00 (geçmişte kaldı, aşağıdaki "Eski tarihler" kuralına bak)
- **Başlık:** `Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ) | Hadîd 1-3 #shorts`
- **Oynatma listesi:** Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ)
- **Etiketler:** `dua,kuran,ayet,kuran ayetleri,dualar,Hadîd suresi,Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ),islam,shorts`
- **Kaynak zip:** `C:\Users\user\OneDrive\Desktop\s1\Allahın 99 ismi 6.zip` → içindeki `vidN05_hadid_1_3.mp4`
- **Açıklama:** Excel'deki F sütununun tamamı (2206 karakter). İlk satırları:
```
Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ)
Hadîd Suresi 1-3. ayetler
```

### Sıra 49
- **Dosya:** `C:\Users\user\OneDrive\Desktop\s1\yuklenecek\0049_vidN06_mucadele_7.mp4`
- **Excel'deki plan:** 2026-11-11 20:00 (geçmişte kaldı, aşağıdaki "Eski tarihler" kuralına bak)
- **Başlık:** `Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ) | Mücâdele 7 #shorts`
- **Oynatma listesi:** Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ)
- **Etiketler:** `dua,kuran,ayet,kuran ayetleri,dualar,Mücâdele suresi,Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ),islam,shorts`
- **Kaynak zip:** `C:\Users\user\OneDrive\Desktop\s1\Allahın 99 ismi 6.zip` → içindeki `vidN06_mucadele_7.mp4`
- **Açıklama:** Excel'deki F sütununun tamamı (2205 karakter). İlk satırları:
```
Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ)
Mücâdele Suresi 7. ayet
```

### Sıra 50
- **Dosya:** `C:\Users\user\OneDrive\Desktop\s1\yuklenecek\0050_vidN07_hasr_20_24.mp4`
- **Excel'deki plan:** 2026-11-11 21:00 (geçmişte kaldı, aşağıdaki "Eski tarihler" kuralına bak)
- **Başlık:** `Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ) | Haşr 20-24 #shorts`
- **Oynatma listesi:** Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ)
- **Etiketler:** `dua,kuran,ayet,kuran ayetleri,dualar,Haşr suresi,Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ),islam,shorts`
- **Kaynak zip:** `C:\Users\user\OneDrive\Desktop\s1\Allahın 99 ismi 6.zip` → içindeki `vidN07_hasr_20_24.mp4`
- **Açıklama:** Excel'deki F sütununun tamamı (2207 karakter). İlk satırları:
```
Allah'ın Güzel İsimleri (Esmâ-ül Hüsnâ)
Haşr Suresi 20-24. ayetler
```

## 10. Bekleyen ayrı iş

- 40 dakikalık uzun sure videosu (~200 MB) Studio'ya yüklenmedi. Bu günlük Shorts akışının parçası değil. **KOMUTA kendiliğinden yüklemesin**, kullanıcıya sorulsun.
