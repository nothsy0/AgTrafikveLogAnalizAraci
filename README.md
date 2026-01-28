# Ağ Trafik ve Log Analiz Aracı

Bu proje, güvenlik duvarı (firewall) loglarını Python kullanarak analiz eden ve ağ üzerindeki anormallikleri tespit etmeye çalışan basit bir **Ağ Trafik ve Log Analiz Aracı (IDS prototipi)** uygular.

## Amaç

- Güvenlik duvarı loglarını (CSV) okuyup ön işleme tabi tutmak
- Trafiğin zamana göre değişimini ve en çok trafik üreten IP adreslerini görselleştirmek
- Basit, **kural tabanlı IDS** kuralları ile:
  - Port taraması (port scan)
  - SSH brute-force denemesi (22/TCP)
  tespiti yapmak
- **Scikit-learn (Isolation Forest)** ile istatistiksel anomali tespiti gerçekleştirmek

## Teknolojiler

- Python 3.x
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn

Gerekli paketler:

```bash
pip install -r requirements.txt
```

## Proje Yapısı

```text
AgTrafikveLogAnalizAraci/
  ├─ data/
  │   ├─ firewall_logs.csv          # Analiz edilen log dosyası (generate_sample_logs.py ile üretilir)
  │   └─ generate_sample_logs.py    # Örnek/sentetik firewall log verisi üretir
  ├─ src/
  │   ├─ log_loader.py              # Log dosyasını yükler ve ön işler
  │   ├─ rule_based_ids.py          # Kural tabanlı IDS fonksiyonları (port scan, SSH brute-force)
  │   ├─ ml_anomaly_detector.py     # Isolation Forest ile anomali tespiti
  │   └─ visualize.py               # Trafik ve IP bazlı görselleştirmeler
  ├─ main.py                        # Uygulamanın giriş noktası
  └─ requirements.txt
```

## Kurulum ve Çalıştırma

```bash
git clone https://github.com/nothsy0/AgTrafikveLogAnalizAracI.git
cd AgTrafikveLogAnalizAraci

pip install -r requirements.txt
```

### 1. Örnek Log Verisi Üretme

Gerçek firewall loglarınız yoksa, proje ile birlikte gelen script ile sentetik veri üretebilirsiniz:

```bash
python data/generate_sample_logs.py
```

Bu komut, `data/firewall_logs.csv` dosyasını oluşturur.

### 2. Ana Aracı Çalıştırma

```bash
python main.py
```

Bu komut:

- Logları okur
- Zamana göre trafik grafiğini çizer
- En çok trafik üreten IP adreslerini görselleştirir
- Kural tabanlı IDS ile port taraması ve SSH brute-force uyarılarını listeler
- Isolation Forest ile anomali tespiti yapar ve toplam anomali sayısını gösterir

## Kural Tabanlı IDS Kuralları (Özet)

- **Port Tarama (Port Scan):**
  - Aynı `src_ip` kısa sürede çok sayıda farklı `dst_port` denerse port taraması olarak işaretlenir.
- **SSH Brute-force (22/TCP):**
  - Belirli bir zaman penceresi (`time_window`) içinde aynı `src_ip` tarafından 22/TCP portuna çok sayıda bağlantı denemesi yapılırsa brute-force şüphesi olarak işaretlenir.

## Anomali Tespiti

- **Algoritma:** Isolation Forest
- Örnek özellikler:
  - `dst_port`
  - `bytes`
- Çıktı:
  - `anomaly_score` kolonu:
    - `1`  → normal
    - `-1` → anomali

## Gelecek Geliştirmeler

- Gerçek firewall logları ile test ve iyileştirmeler
- Daha gelişmiş özellik seti (IP sayısı, bağlantı sıklığı, hata kodları vb.)
- Web tabanlı dashboard ile canlı takip
- Tespit edilen saldırılar için e-posta / webhook bildirimleri

---

Bu proje, siber güvenlik stajında edinilen bilgilerin pratiğe dökülmesi ve log analizi / IDS kavramlarının temel düzeyde uygulanmasını hedefleyen bir örnek çalışma olarak tasarlanmıştır.

