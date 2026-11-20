# A9E-10 AWS起点の設定とPLC指令

## 仕様と根拠

| 用途 | AWSの仕様と根拠 |
|---|---|
| コンポーネントと配備に連動する設定 | Greengrass Deploymentでコンポーネント用設定のリセット・マージを指定できる。ファイル生成や適用時の検証はコンポーネント側で設計する。[AWS コンポーネント設定の更新](https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html) |
| 設定状態の同期 | Device Shadowは `desired`、`reported`、差分、ドキュメントの版を持つ。構成ファイル本体を別途配布する場合は、取得先、版、ハッシュ等の配布方法を設計する。[AWS Device Shadowのドキュメント](https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-document.html) |
| 単発の指令と結果 | AWS IoT Device Management Commandsは端末への指令と実行状態を扱う。独自のMQTTメッセージを採用する場合、GreengrassのAWS IoT Core MQTT IPCを使って購読・発行でき、コンポーネントのIPC認可設定が必要。[AWS IoT Device Management commands](https://docs.aws.amazon.com/iot/latest/developerguide/iot-remote-command.html) [AWS IoT Core MQTT IPC](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-iot-core-mqtt.html) |

## レビュー観点

- 設定変更は版・スキーマ・適用対象を最初に検証し、検証済みの版を切り替え、成功時に適用版を報告する。古い版や失敗時の復旧を定義する。継続的な目標状態と一回限りの動作を識別し、再接続時に古い指令が作用しないようにする。
- 指令は端末、PLC、論理的な書き込み項目、値・範囲、期限、指令IDを照合する。書き込み対象は事前に定義した項目に限定し、許可・インターロックはPLC側でも確認する。PLCの安全制御や非常停止はクラウド通信に依存させない。
- 受領、検証拒否、実行中、適用確認、失敗、結果不明といった状態を区別し、成功の定義を決める。PLCの物理動作を伴う場合はPLC側の完了条件まで確認し、AWSへの応答には指令IDと結果を紐付ける。
- 指令ID、状態、必要ならPLC側の適用済み連番を用いて重複・再起動・順序逆転を処理する。PLC書き込み成立からローカル結果保存までの間に停電する場合は端末DBだけで一回限りの実行を保証できない。PLC側で照合できない命令は結果不明として扱い、再送・再実行の条件を決める。[A9E-03](A9E-03-persistence.md) [A9E-08](A9E-08-modbus.md)
- 端末ごとのIoT認証、AWSポリシー／IAM、Greengrass IPC認可、アプリの検証を確認する。受け取った内容で任意コマンドを起動したり任意アドレスへ書き込んだりできる設計を避け、証跡を残す。
