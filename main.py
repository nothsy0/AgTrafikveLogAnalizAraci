from pathlib import Path

from src.log_loader import load_firewall_logs
from src.rule_based_ids import detect_port_scan, detect_bruteforce_ssh
from src.ml_anomaly_detector import run_isolation_forest
from src.visualize import plot_traffic_over_time, plot_top_talkers


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "firewall_logs.csv"


def main() -> None:
    if not DATA_PATH.exists():
        print(f\"Log dosyası bulunamadı: {DATA_PATH}\")
        print(\"Önce 'data/generate_sample_logs.py' dosyasını çalıştırarak örnek veri üretebilirsin.\")
        return

    df = load_firewall_logs(str(DATA_PATH))
    print(f\"Toplam log kaydı: {len(df)}\")

    # Görselleştirme
    plot_traffic_over_time(df)
    plot_top_talkers(df)

    # Kural tabanlı IDS
    port_scan_alerts = detect_port_scan(df)
    ssh_bruteforce_alerts = detect_bruteforce_ssh(df)

    print(\"\\n[PORT SCAN UYARILARI]\")
    if port_scan_alerts.empty:
        print(\"Port scan tespit edilmedi.\")
    else:
        print(port_scan_alerts[[\"timestamp\", \"src_ip\", \"dst_ip\", \"dst_port\", \"alert_type\"]].head())

    print(\"\\n[SSH BRUTE-FORCE UYARILARI]\")
    if ssh_bruteforce_alerts.empty:
        print(\"SSH brute-force saldırısı tespit edilmedi.\")
    else:
        print(ssh_bruteforce_alerts[[\"timestamp\", \"src_ip\", \"dst_ip\", \"dst_port\", \"alert_type\"]].head())

    # ML tabanlı anomali tespiti
    df_with_anomaly = run_isolation_forest(df)
    anomalies = df_with_anomaly[df_with_anomaly[\"anomaly_score\"] == -1]
    print(f\"\\nTespit edilen anomali sayısı: {len(anomalies)}\")


if __name__ == \"__main__\":
    main()

