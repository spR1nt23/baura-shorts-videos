# Macikuri TV — üretim reçetesi

İngilizce, animasyonlu korku hikâyeleri. YouTube: "Macikuri TV", Studio kanal `UCyAOn8nydPG6phjYMRs7i-Q`, Google hesabı asil.arica34.
Maskot: Maçikuri — eski bir tüplü televizyonun içinde yaşayan gölge yaratık (tek gözü sarı, tek gözü kırmızı, dikişli gülüş). Her videonun girişinde (render.py otomatik ekler) televizyon parazitiyle belirir.

## Haftalık dizi planı (EN ÖNEMLİ KURAL)
Her hafta tek bir korku DİZİSİ: Pazartesi–Cumartesi her gün 2 bölüm (19:00 ve 23:00 TR) = 12 bölüm, Pazar 12:00'de final bölümü yoksa sadece birleşik video. **Pazar 20:00: haftanın bütün bölümleri tek uzun yatay video** ("<Dizi adı> (Full Story)").
- Sezon planı `series/<YYYY>-W<hafta>-<slug>.md` dosyasında: bölüm tablosu (tarih/saat, olay, cliffhanger). O haftanın dosyası yoksa (Pazartesi) önce 12 bölümlük planı yaz ve pushla; sonra o günün bölümlerini üret. Plan tutarlı bir hikâye: sabit anlatıcı, sabit mekân(lar), kuralları olan bir tehdit, her bölüm yeni bir ipucu, 6. ve 9. bölümde büyük ters köşe, final döngüyle kapanır.
- Her bölüm 40–55 sn, 4–6 sahne. İlk cümle önceki bölümü 1 cümlede hatırlatır ("Last night I found Walt's badge."). Son cümle = tablodaki cliffhanger.
- spec.json'a `"series": "<Dizi adı>", "episode": N, "total": <toplam>` ekle → render.py girişe "<DİZİ> · PART N", sona "PART N+1 TOMORROW" (finalde "THE END") kartını koyar. Cumartesi 23:00 bölümünde `"next": "SUNDAY"`.
- Çizim sürekliliği: aynı karakter her bölümde aynı renk/kıyafet/silüet; mekân SVG'lerini `series/<slug>/` altına kaydet ve sonraki bölümlerde yeniden kullan (kopyalayıp değiştir).
- Dosyalar: `macikuri/<targetDate>/ep<NN>.mp4` (NN = bölüm no, iki hane).
- Başlık: `<Dizi adı> — Part N 😨 #scarystories #horror` (finalde `FINAL`). Açıklamanın ilk satırı: "Part N of <Dizi adı>. New part every day at 7PM & 11PM (Turkey) — full story on Sunday."
- Yayın: publishAt = targetDate 19:00 ve 23:00 (+03:00).

### Pazar (targetDate Pazar ise)
1. Final bölümü varsa üret (12:00).
2. `python3 tools/compile.py /tmp/full.mp4 macikuri/<Pzt>/ep01.mp4 … macikuri/<Pazar>/epNN.mp4` (haftanın bütün bölümleri, sırayla; dosyalar depoda).
3. `macikuri/<targetDate>/full.mp4` olarak pushla. format "long", publishAt targetDate 20:00, başlık `<Dizi adı> (Full Story) | Animated Horror Story`, açıklamada bölüm zamanları (chapters: 0:00 Part 1 …; her bölüm ~süresi), kapak: yoksa son bölümün en ürkütücü karesi (ffmpeg ile 1280x720 kare + "FULL STORY" yazısı) → extra.thumbnailUrl.

## Kurulum ve render
```
cd baura-shorts-videos/kanallar/macikuri && bash tools/setup.sh
python3 tools/render.py content/<targetDate>/short1/spec.json /tmp/short1.mp4   # ~8 dk
```
Çıkan videoyu `macikuri/<targetDate>/short<N>.mp4` olarak baura-shorts-videos main dalına koy.
Kontrol: `ffprobe` ile 1080x1920, 45–58 sn; 6 kare çıkarıp bak (sahne sırası, altyazı okunuyor mu, çizim boş/bozuk değil mi).

## Hikâye kuralları
- ÖZGÜN kurgu. Gerçek kişi, gerçek suç, gerçek kurban YOK. Bilinen creepypasta karakterleri (Slenderman vb.) ve film/dizi karakterleri YOK.
- Birinci ağızdan, sade İngilizce, kısa cümleler. 110–135 kelime (≈50 sn). 5–7 sahne, her sahne 1–3 cümle.
- İlk cümle kanca: sıradan bir yer + saat/ayrıntı ("I used to work the night shift at…").
- Son sahne twist ile biter; son cümle ürpertici kısa bir kapanış. Ayrı "abone ol" cümlesi YOK.
- Vurgulanacak kelimeyi BÜYÜK yaz (altyazıda sarı yanar): `Something TALL was standing…`
- Konu havuzu: gece vardiyaları (benzin istasyonu, otel resepsiyonu, hastane, güvenlik), bebek monitörü, kamp, asansör, kiralık ev, eski oyun konsolu, otoyol durağı, yanlış numara, metro son sefer, çatı katı, kar fırtınasında kulübe, kayıp kedi ilanı, apartman kapısındaki gözetleme deliği… Kullanılanları `TOPICS.md`'ye yaz, tekrar etme.
- Şiddet ve kan gösterme; korku atmosferle, gölgeyle, ima ile. Çocuklara yönelik değil ama gore yok.

## Çizim kuralları (her sahne bir SVG, viewBox `0 0 1080 1920`)
- Düz şekillerle karanlık çizgi film tarzı (örnek: `example/s1.svg … s6.svg` — üslubu buna benzet).
- Palet: zemin #05040b / #101418 / #1b1430, floresan yeşil #a8ffd0 / #d9ffe9 (düşük opaklık ışık), ten #c9b8a6, yaratık siyah #000 + kırmızı göz #ff3b3b, vurgu sarı #f4ff9a.
- Ana obje ekranın orta 1/3'ünde; alt %25'e önemli şey koyma (altyazı alanı y≈1340).
- render.py görüntüyü %25 büyütüp kırpar: kenarlara önemli şey koyma.
- Yazı gerekiyorsa font-family "Bebas Neue" veya "Creepster". Gerçek marka/logo YOK.
- Her sahneye `move` (in/out/left/right/up/down) ve gerekirse `fx` (flicker, shake, red, static) ver. Gerilim sahnesinde flicker/shake, monitör/TV sahnesinde static, son sahnede red.

## spec.json
`example/spec.json` biçiminde: `{"format":"short","voice":"bm_george","speed":0.92,"scenes":[{"svg_file":"s1.svg","move":"in","fx":[],"vo":"..."}]}`

## Başlık / açıklama / etiket
- Başlık: kısa merak cümlesi + emoji + 2 hashtag, ≤70 karakter. Örn: `The Night Shift Camera Saw Something 😨 #scarystories #horror`
- Açıklama:
```
<hikâyenin ilk cümlesi ya da merak cümlesi>

📺 Macikuri TV — animated scary stories, new every day.
🔔 Subscribe if you're brave enough.
All stories are original fiction.

#scarystories #horrorstories #animatedhorror #creepy #shorts
```
- Etiketler: scary stories, horror stories, animated horror, creepy stories, scary story animated, horror shorts, + konuya özel 3 etiket.

## Studio yükleme ayarları (yükleme görevi için)
Dil English, kategori "Film & Animation", "Hayır, çocuklara özel değil", Gelişmiş ayarlar → yapay zekâ/sentetik içerik: **Evet** (yapay ses). publishAt'e göre planla.
