# 要素索引

| ID | 要素 | 検索語 |
|---|---|---|
| [A9E-01](A9E-01-hardware.md) | 本体・型番・インターフェース | CPU Cortex-A35 ARM64 aarch64 メモリ RAM eMMC microSD USB RS-485 接点 電源 温度 |
| [A9E-02](A9E-02-abos-runtime.md) | ABOSとPodman実行環境 | Alpine musl OpenRC systemd overlayfs tmpfs OCI 自動起動 set_command add_volumes |
| [A9E-03](A9E-03-persistence.md) | 永続領域とデータの復旧 | volumes rollback ロールバック persist_file Btrfs CoW 再起動 停電 CSV キュー 重複排除 |
| [A9E-04](A9E-04-network.md) | PLC側・AWS側ネットワークと時刻 | Ethernet LAN LTE WLAN nmcli IP ルーティング NAT DNS NTP chronyd RTC ファイアウォール |
| [A9E-05](A9E-05-update.md) | 更新・量産・復旧 | SWUpdate SWU mkswu A/B 署名 ロールバック 量産 インストールディスク 保守 |
| [A9E-06](A9E-06-operations.md) | 運用監視・障害試験・認証 | ログ ヘルスチェック watchdog 死活 eMMC SE050 秘密鍵 停電 容量不足 |
| [A9E-07](A9E-07-greengrass.md) | Greengrass V2の導入・コンポーネント | nucleus lite glibc Java Docker systemd Podman recipe Run IPC サポート |
| [A9E-08](A9E-08-modbus.md) | PLCとのModbus TCP通信 | 502 TCP RTU レジスタ Unit ID エンディアン ポーリング タイムアウト 読戻し |
| [A9E-09](A9E-09-csv-upload.md) | CSVの蓄積とAWSへの送信 | S3 Stream Manager spool ファイル ローテーション 再送 オフライン バックログ |
| [A9E-10](A9E-10-cloud-downlink.md) | AWS起点の設定・PLC指令 | 配備 Deployment Shadow Commands MQTT IPC ACK 指令 TTL commandId インターロック |

## 出典

- **M** は添付のアットマークテクノ『Armadillo-IoT ゲートウェイ A9E 製品マニュアル』v1.18.0（2026-10-28、日本語版、`armadillo-iotg-a9e_product_manual_ja-1.18.0.pdf`）。記載の p./pp. は誌面ページ。採録した範囲ではPDFページ番号と一致する。参照時は対象版を選ぶ。[公式マニュアル配布ページ](https://armadillo.atmark-techno.com/resources/documents/armadillo-iot-a9e/manuals) [v1.18.0 リリース告知](https://armadillo.atmark-techno.com/news/20261028/update-aiota9e)
- AWSとModbusの根拠は各要素に掲載。AWSのオンライン文書は更新されるため、サポート・依存バージョン・リージョン・制約が判断を左右する場合は回答時に公式文書を再確認する。
- 対象機の型番・ABOS版、採用するGreengrassと各コンポーネントのバージョン、PLCの型番・ファームウェアを適用条件として扱う。PLC固有のレジスタ仕様は対象PLCのメーカー資料を根拠にする。
