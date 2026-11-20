# 構成レビュー例

## 相談の前提

A9E/ABOSにGreengrass V2を導入し、カスタムコンポーネントがPLCをModbus TCPでポーリングしてCSVを生成する。CSVの定期送信先としてS3を仮定する。AWSからは設定変更とPLCへの指令を受ける。

## 結論

PLCとのTCP通信とCSV永続化に使えるA9Eの製品機能は確認できる。Greengrass V2の採用判断は、対象ABOS版でのランタイム適合性と、停電後のCSV・指令の復旧を確認してから行う。最初の実機試験では収集と送信までを確認し、書き込みはテスト用PLCまたはシミュレーターで状態遷移を確認する。[A9E-02](A9E-02-abos-runtime.md) [A9E-07](A9E-07-greengrass.md) [A9E-08](A9E-08-modbus.md) [A9E-09](A9E-09-csv-upload.md)

| 論点 | 根拠付きの判断 | 確認方法 |
|---|---|---|
| Greengrassの実行環境 | 標準nucleusはJRE・glibcを要求する。ABOSのアプリ実行方式に沿い、ARM用でglibcを備えるコンテナを評価候補とする。AWS公式Docker手順とPodman構成の適合性は対象版で確認する。[A9E-07](A9E-07-greengrass.md) [AWS nucleusの要件](https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-nucleus-component.html) | 対象版で起動、配備、自動起動、再接続、更新中のリソース使用量とサポート条件を確認する。 |
| PLC通信経路 | A9Eの有線LANは1ポート。PLC側とAWS向けの経路を定義し、Modbus TCPクライアントはコンポーネントで用意する。型番によってLTE/WLANの有無が異なる。[A9E-04](A9E-04-network.md) [A9E-08](A9E-08-modbus.md) [M](index.md) §2.3 表2.3–2.5 pp.49–51、§6.10.1 p.422 | 対象PLCのレジスタ表を使い、コンテナからの疎通、異常応答、タイムアウト、WAN断中の収集を確認する。 |
| CSV保存と送信 | 未送信CSVと送信台帳はABOSのロールバックで戻らない領域に置く。確定済みファイルのみを対象にし、AWS側の成功確認後に削除する。[A9E-09](A9E-09-csv-upload.md) [M](index.md) §3.3.5.1 表3.4 p.115 | 長時間WAN断、容量上限、送信直後の停電、再送時の重複を試験する。 |
| 設定と指令 | 設定は配備設定または状態同期で版管理する。単発指令は期限、指令ID、PLC側の完了条件を持たせる。結果不明を扱う設計が必要。[A9E-10](A9E-10-cloud-downlink.md) [AWS Device Shadow](https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-document.html) [AWS Commands](https://docs.aws.amazon.com/iot/latest/developerguide/iot-remote-command.html) | 古い版、期限切れ、重複、通信応答喪失、書き込み直後の停電を個別に試験する。 |

### PLCで書き込みが成立し、応答前に通信が切れた場合

| 時点 | Gatewayで保持する状態 | 復旧時の扱い |
|---|---|---|
| 受領・検証後 | 指令ID、対象、期限、受付状態を永続化 | 期限と対象を再確認する |
| 書き込みを試行する直前 | 同じ指令IDで実行中を記録 | 実行済みの可能性を考慮する |
| 応答喪失・電源断 | 結果不明。再起動直後には実行中の記録が残る場合がある | PLCの適用済みIDや完了状態を照合する。照合不能の場合は結果不明を返す |
| PLC側で適用の確認後 | 確定結果を永続化する | AWSへの結果通知が失敗した場合は、保存済み結果を再通知する |

必要な前提はA9E型番とABOS版、PLC型番とレジスタ表、WAN経路、CSV生成量・最大オフライン時間・許容欠損、PLCで指令が起こす作用と適用確認の方法。
