# Vice City Daily (GTA 6 haber Shorts) — günlük üretim

**Kanal:** Vice City Daily (@GTASixDailyNews), Studio kanal ID `UCN3MaVtpp_xh31FcYaE3kNg`.
**İçerik:** İngilizce GTA 6 haberleri, fragman detayları, gizli ayrıntılar, çıkış (19 Kasım 2026) ve sonrası güncellemeler. Hedef kitle ABD.
**Hayran kanalıdır:** Rockstar/GTA logosu, resmi kapak/fragman görüntüsü, oyun ekran görüntüsü, gerçek kişi fotoğrafı KULLANILMAZ (telif ve marka). Görseller tamamen özgün: düz ikonlar, gradyan arka planlar, büyük başlıklar.

## Günlük plan
- Hedef gün başına **3 Short** (35–55 sn). Yayın saatleri (Türkiye): **16:00, 21:00** ve **ertesi gün 02:00** (ABD sabah / öğle / akşam).
- Dosyalar: spR1nt23/baura-shorts-videos `main` dalında `gta6/<targetDate>/gta6_<n>.mp4`. Raw URL: `https://raw.githubusercontent.com/spR1nt23/baura-shorts-videos/main/gta6/<targetDate>/gta6_<n>.mp4`.
- İşlenen konular: bu klasördeki `TOPICS.md` (yoksa oluştur). Aynı haberi tekrar etme; aynı konuyu farklı açıdan işlemek serbest.

## Araç: Secret Spawn hattı (aynısını kullan)
```bash
git clone --depth 1 https://github.com/spR1nt23/secret-spawn-videos.git /tmp/ss && cd /tmp/ss && bash tools/setup.sh
```
- Sadece Short üret (`short1 short2 short3`), uzun video yok. Şablon: `content/TEMPLATE.py`; kurallar secret-spawn-videos/WORKFLOW.md bölüm 4–8 (senaryo, TTS, render, kare kontrolü) aynen geçerli.
- **Markayı değiştir:** render/thumbnail kodundaki "SECRET SPAWN NEWS" üst yazısını **"VICE CITY DAILY"** yap; "● BREAKING" hapı kalabilir. Outro'da "subscribe to Vice City Daily".
- **Renkler:** Vice City paleti — arka planda mor/lacivert (`violet`, `navy`, `purple`), vurgular `pink`, `orange`, `yellow` (gün batımı) ve turkuaz hissi için `blue`/`green`.
- Ses: `am_michael`, hız 1.12.
- İkonlar: palmiye, güneş, araba, harita pini, takvim, kontrolcü, para, polis siren vb. — gerekirse `icons.py`'ye aynı düz stilde ekle. GTA logosu/karakteri çizilmez.

## Araştırma (zorunlu, web'den doğrula)
Öncelik: rockstargames.com/newswire → Rockstar'ın resmi X/Instagram duyuruları → IGN, GameSpot, Eurogamer, Polygon, The Verge, Kotaku, VGC, Insider Gaming (sızıntılarda "reportedly"/"rumor" diye belirt).
- Her maddede en az bir güvenilir kaynak olsun; tarih ver ("on Nov 14").
- Uydurma bilgi, kesinleşmemiş tarih ya da sızıntıyı gerçek gibi sunma YOK.
- Çıkıştan önce: fragman detayları, ön sipariş/sürümler, harita (Leonida, Vice City), karakterler (Lucia, Jason), çıkış saatleri, platformlar. Çıkıştan sonra: ipuçları, gizli yerler, rekorlar, güncellemeler, topluluk keşifleri.

## Başlık / açıklama
- Başlık (≤100 karakter, merak uyandırıcı, clickbait değil): örn. `GTA 6 Just Confirmed This Huge Detail 🌴 #gta6 #shorts`
- Açıklama:
```
<1–2 cümle özet>

Sources: <kaynak adları>
Unofficial fan channel — not affiliated with Rockstar Games or Take-Two.

#GTA6 #GTAVI #GTA6News #ViceCity #Leonida #RockstarGames #shorts
```
- Etiketler: gta 6, gta vi, gta 6 news, gta 6 trailer, vice city, leonida, rockstar games, gta 6 release, grand theft auto 6

## Studio yükleme ayarları (işçi görevi için)
- Kanal: Vice City Daily `UCN3MaVtpp_xh31FcYaE3kNg` (doğru kanal seçili mi doğrula).
- "Hayır, çocuklara özel değil". Dil: English. Kategori: Gaming.
- Gelişmiş ayarlar → "Altered or synthetic content" (yapay zeka): **Evet** (AI seslendirme).
- publishAt saatine planla.
