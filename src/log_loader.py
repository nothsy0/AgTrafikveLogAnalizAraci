import pandas as pd


def load_firewall_logs(path: str) -> pd.DataFrame:
    """
    Güvenlik duvarı loglarını CSV dosyasından okur ve temel ön işleme uygular.

    Beklenen kolonlar (önerilen):
        - timestamp
        - src_ip
        - dst_ip
        - src_port
        - dst_port
        - protocol
        - action
        - bytes
    """
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp")
    return df

