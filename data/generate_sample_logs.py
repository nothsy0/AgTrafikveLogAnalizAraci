import csv
import random
from datetime import datetime, timedelta


def generate_sample_firewall_logs(path: str, num_rows: int = 1000) -> None:
    """
    Örnek firewall log verisi üretir.
    Gerçek logların yoksa proje için sentetik veri üretebilirsin.
    """
    start_time = datetime.now() - timedelta(hours=1)

    src_ips = [f"192.168.1.{i}" for i in range(2, 50)]
    dst_ips = ["8.8.8.8", "1.1.1.1", "10.0.0.1"]
    ports = [22, 53, 80, 443, 8080, 3306]
    protocols = ["TCP", "UDP"]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "timestamp",
                "src_ip",
                "dst_ip",
                "src_port",
                "dst_port",
                "protocol",
                "action",
                "bytes",
            ]
        )

        current_time = start_time
        for _ in range(num_rows):
            current_time += timedelta(seconds=random.randint(1, 5))

            src_ip = random.choice(src_ips)
            dst_ip = random.choice(dst_ips)
            src_port = random.randint(1024, 65535)
            dst_port = random.choice(ports)
            protocol = random.choice(protocols)
            action = random.choice(["ALLOW", "DENY"])
            bytes_count = random.randint(40, 5000)

            writer.writerow(
                [
                    current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    src_ip,
                    dst_ip,
                    src_port,
                    dst_port,
                    protocol,
                    action,
                    bytes_count,
                ]
            )


if __name__ == "__main__":
    generate_sample_firewall_logs("firewall_logs.csv", num_rows=2000)

