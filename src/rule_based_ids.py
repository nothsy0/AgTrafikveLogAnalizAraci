import pandas as pd


def detect_port_scan(df: pd.DataFrame, threshold: int = 20) -> pd.DataFrame:
    """
    Basit kural:
      Aynı src_ip kısa sürede çok fazla farklı dst_port deniyorsa port taraması ihtimali vardır.

    threshold: Bir IP'nin denediği farklı hedef port sayısı eşiği.
    """
    # Her src_ip için kaç farklı hedef port denendiğine bakalım
    counts = df.groupby("src_ip")["dst_port"].nunique().reset_index()
    suspicious_ips = counts[counts["dst_port"] >= threshold]["src_ip"]

    alerts = df[df["src_ip"].isin(suspicious_ips)].copy()
    if not alerts.empty:
        alerts["alert_type"] = "PORT_SCAN"
    return alerts


def detect_bruteforce_ssh(
    df: pd.DataFrame, time_window: str = "5min", attempts_threshold: int = 10
) -> pd.DataFrame:
    """
    Basit kural:
      22/TCP portuna belirli bir zaman penceresi içinde çok sayıda bağlantı denemesi varsa
      SSH brute-force saldırısı olabilir.

    time_window: Pandas offset string (ör: '5min', '10min')
    attempts_threshold: Pencere içinde izin verilen maksimum deneme sayısı.
    """
    ssh_df = df[(df["dst_port"] == 22) & (df["protocol"].str.upper() == "TCP")].copy()
    if ssh_df.empty:
        return pd.DataFrame(columns=list(df.columns) + ["alert_type"])

    ssh_df = ssh_df.set_index("timestamp")

    alerts_list = []
    for src_ip, group in ssh_df.groupby("src_ip"):
        # Her istek için, önceki time_window içindeki istek sayısını hesapla
        counts = group["action"].rolling(time_window).count()
        suspicious = group[counts >= attempts_threshold]
        if not suspicious.empty:
            tmp = suspicious.copy()
            tmp["alert_type"] = "SSH_BRUTEFORCE"
            alerts_list.append(tmp)

    if alerts_list:
        result = pd.concat(alerts_list).reset_index()
        return result

    return pd.DataFrame(columns=list(df.columns) + ["alert_type"])

