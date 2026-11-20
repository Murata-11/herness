# A9E-04 ネットワークと時刻

## 仕様と根拠

- A9EのCON2は10BASE-T/100BASE-TX、AUTO-MDIXの有線LAN。ABOSはABOS Webとコマンドラインのネットワーク設定を提供する。複数インターフェースが有効な場合、ルーティング次第で疎通の確認先と実際の経路が異なる。[M](index.md) §3.6.2 pp.149–150、§3.8.7–3.8.14 pp.209–230、§6.16 pp.522–543、特に§6.16.4 p.527。
- Podmanは個別のコンテナIPを割り当てられる。既定のネットワーク帯は10.88.0.0/16。起動設定ではユーザー定義ネットワーク、`host`、`none` を選択できる。[M](index.md) §6.9.4.8 pp.406–407、§6.9.7 pp.415–417。
- ABOSのNTPクライアントはchronyd。設定は `/etc/chrony/conf.d/` で上書きできる。RTCはバックアップ用電池CR1220を接続できる。搭載状態・初期値は現物で確認する。[M](index.md) §3.6.14 pp.176–179、§3.12 pp.241–242。

## レビュー観点

- PLC宛経路とAWS向けデフォルト経路、DNS、NTP、ファイアウォールを設計し、コンテナ内から両方を検証する。PLC側とPodman側のアドレス帯の重複、LTE再接続や経路切替後の既存TCP接続の復旧も見る。
- PLCのModbusポートは必要なローカル通信元に限定し、インターネットへ公開しない。AWSへのアウトバウンドの宛先・ポートは採用機能とリージョンのAWS要件で確認する。[AWS Greengrassのプロキシ／ファイアウォール要件](https://docs.aws.amazon.com/greengrass/v2/developerguide/allow-device-traffic.html)
- CSV時刻、TLSに使う実時刻、タイムアウトを測る単調時計の用途を定義する。NTP未同期時の品質フラグや記録可否、期限がある指令の保留・拒否条件を決める。[A9E-09](A9E-09-csv-upload.md) [A9E-10](A9E-10-cloud-downlink.md)
