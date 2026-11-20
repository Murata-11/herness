# A9E-08 PLCとのModbus TCP通信

## 仕様と根拠

- A9EにはEthernetがある。メーカーのゲートウェイコンテナで記載されたModbus機能はRS-485のModbus RTUレジスタ読み出し。対象PLCとのModbus TCPは採用するコンポーネントとPLCの対応仕様を別途確認する。[M](index.md) §3.6.2 pp.149–150、§6.10.1 p.422。
- Modbus TCPはクライアント／サーバーの要求・応答で、MBAPヘッダにTransaction IdentifierとUnit Identifierを持つ。標準ポートはTCP 502。プロトコル資料はデータモデル・機能コード・例外応答を定義する。具体的なレジスタ、32ビット値のワード順、接続制限と対応機能はPLCメーカーの仕様に依存する。[Modbus TCP Implementation Guide v1.0b](https://www.modbus.org/docs/Modbus_Messaging_Implementation_Guide_V1_0b.pdf) [Modbus Application Protocol v1.1b3](https://www.modbus.org/file/secure/modbusprotocolspecification.pdf)

## レビュー観点

- A9Eがクライアント、PLCがサーバーという前提を確認する。型番・ファームウェア、PLC側のレジスタ表、0始まりアドレスと表記上の番号の対応、Unit ID、読み書き対象、符号、スケール、ワード順を確認する。
- ポーリング周期に対し、要求の締切、再接続、再試行上限、読み取りと書き込みの調停を定義する。タイムアウト時の値に品質フラグや取得時刻を持たせ、以前の値を今回の取得値として扱わない。
- 書き込みの応答喪失時は、書き込みがPLCで成立した可能性がある。PLC側の状態・処理履歴を確認して照合し、実行済みか判断不能な命令を無条件で再送しない。必要な読戻しや適用完了フラグはPLC側仕様と合意する。[A9E-10](A9E-10-cloud-downlink.md)
