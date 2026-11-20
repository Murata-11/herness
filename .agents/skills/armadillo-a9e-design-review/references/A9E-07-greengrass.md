# A9E-07 Greengrass V2の導入とコンポーネント

## 仕様と根拠

- ABOSはPodmanによるアプリ実行を基本とする。メーカーのゲートウェイコンテナではAWS IoT Core接続例が示されている。Greengrass V2をA9Eの対象ABOS版で導入・サポートできるかは、その記載から判断できない。[M](index.md) §3.7.2 pp.193–194、§6.10.1 pp.422–423、§6.10.5 pp.424–434。
- AWSの標準Java nucleusのLinux要件には、JRE 8以上、glibc 2.25以上、コア用RAM 96 MB以上、ディスク空き256 MB以上が含まれる。RAMとディスクの最低値にコンポーネント分は含まれない。Armv8（AArch64）はAWSの対応アーキテクチャに含まれる。標準nucleusでの `systemctl` はサービス登録時のオプション。対象バージョンの全要件を照合する。[AWS Greengrass nucleus](https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-nucleus-component.html)
- AWSのCoreコンテナ手順はDocker Engineを前提とし、公開Dockerfileの説明はx86_64ベース。ABOSのPodman上でのARM用構成には追加の適合確認が必要。nucleus liteは別ランタイムで、公式ページはsystemd搭載Linuxを記載している。採用時は利用するコンポーネントとIPCの互換性を確認する。[AWS CoreのDocker実行](https://docs.aws.amazon.com/greengrass/v2/developerguide/run-greengrass-docker.html) [AWS Greengrass nucleus lite](https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-nucleus-lite-component.html)
- カスタムコンポーネントのRecipeでプラットフォーム別のManifest、アーティファクト、依存関係、ライフサイクル、設定を定義できる。[AWS Component recipe reference](https://docs.aws.amazon.com/greengrass/v2/developerguide/component-recipe-reference.html)

## レビュー観点

- 標準nucleusをA9E上で動かす候補として、glibcを備えたARM用コンテナとPodmanによる起動を評価する。AWSとメーカーのサポート条件は対象版・方式で確認し、PoC結果と区別する。
- 対象機でランタイム起動、コンポーネント配備・実行、権限降格、証明書での接続、再起動後の再接続、停止シグナル、ログ保持、無線切断時の継続を試す。コア、収集、送信、更新が重なる条件でメモリ・空きディスクを測る。
- PLC収集、CSV送信、設定／指令受信は障害の影響範囲を定義する。別コンポーネントにする場合も、PLCへの書き込みを許可・実行する責任を一箇所に集約する。[A9E-08](A9E-08-modbus.md) [A9E-10](A9E-10-cloud-downlink.md)
