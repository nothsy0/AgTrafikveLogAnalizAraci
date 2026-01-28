import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_traffic_over_time(df: pd.DataFrame, freq: str = "5min") -> None:
    """
    Zamana göre toplam trafik miktarını çizer.
    """
    if df.empty:
        print("Veri boş, grafik çizilemiyor.")
        return

    traffic = df.set_index("timestamp").resample(freq)["bytes"].sum()
    plt.figure(figsize=(10, 4))
    traffic.plot()
    plt.title("Zamana Göre Toplam Trafik (bytes)")
    plt.xlabel("Zaman")
    plt.ylabel("Bytes")
    plt.tight_layout()
    plt.show()


def plot_top_talkers(df: pd.DataFrame, n: int = 10) -> None:
    """
    En çok trafik üreten kaynak IP adreslerini çizer.
    """
    if df.empty:
        print("Veri boş, grafik çizilemiyor.")
        return

    top_src = df.groupby("src_ip")["bytes"].sum().nlargest(n)
    plt.figure(figsize=(8, 4))
    sns.barplot(x=top_src.values, y=top_src.index, orient="h")
    plt.title(f"En Çok Trafik Üreten {n} Kaynak IP")
    plt.xlabel("Bytes")
    plt.ylabel("Kaynak IP")
    plt.tight_layout()
    plt.show()

