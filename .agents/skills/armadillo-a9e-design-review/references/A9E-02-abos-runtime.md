# A9E-02 ABOSとPodmanの実行環境

## 仕様と根拠

- ABOSのベースはAlpine Linuxで、ユーザーアプリは基本的にPodmanコンテナ内で動作する。ホストrootfsはoverlayfsで、通常の変更は電源断後に保持されない。開発時の個別保持には `persist_file`、運用での更新にはSWUpdateを使う。ホストのサービス管理例はOpenRC（`rc-service`、`rc-update`）。[M](index.md) §3.3.1 p.107、§3.3.4.5–3.3.5 pp.113–115、§3.7.2 pp.193–194、§3.12 p.241、§6.29.3 pp.577–580。
- `/etc/atmark/containers/*.conf` によるブート時自動起動と、起動設定の `add_volumes` によるホスト領域のマウントを利用できる。再起動方針、ヘルスチェック、自動起動の無効化も設定できる。コンテナの起動設定とGreengrassのコンポーネントRecipeは別の管理単位。[M](index.md) §6.9.4 pp.402–410。
- ABOSはDebian GNU/Linuxベースのコンテナイメージも提供する。コンテナのユーザーランドを選んでも、ホスト側のネットワーク、起動・更新方式やカーネルの制約は引き継ぐ。[M](index.md) §3.7.2 pp.193–194、§6.9.5 pp.412–415。

## レビュー観点

- Greengrassの配置を決めてから、JRE、glibc/musl、ユーザーとsudo、シグナル伝播、コンポーネント起動・停止を確認する。[A9E-07](A9E-07-greengrass.md)
- コンテナの書き込み層にランタイム状態やCSVを置く場合は、再生成後の保持を検証する。必要な状態には明示的なボリュームを割り当て、マウント権限と更新時の扱いを確認する。[A9E-03](A9E-03-persistence.md)
