# claim-lint
ローカル環境で公開前のドキュメントに含まれる誇張表現と非公開の機密用語を決定論的に検出する Markdown リンター

ご注意：本プロジェクトは実験的（experimental）なローカル専用のプロトタイプツールであり、実環境における需要の検証や本番運用向け（production-ready）の位置付けではありません。

AIエージェントによるドキュメント生成フローでは、公開告知文章（READMEやケーススタディ）の作成後に、証拠のない誇張表現や内部機密用語の漏洩が混ざっていないかを公開前に確認したくなる場面があります。claim-lint は、その確認をローカルの明示ルールで行うための実験的な CLI です。

## what it checks
claim-lint は以下の項目をスキャンします：
- prohibited_claims: 実証証跡のないパフォーマンスや利便性の主張表現（例: エビデンスのない大幅な時間短縮、生産性向上の文言）。
- internal_names: 非公開のプロジェクト名、内部システム名、コードネーム。

## 30-second quick start
本ツールはローカルのコマンドラインから直接実行できます。

1. カレントディレクトリに設定ファイル .claimlintrc.json を配置します。
2. ドキュメントをスキャンします：
```bash
claim-lint scan README.md
```

## config example
カレントディレクトリ直下の .claimlintrc.json にルールを定義します。本バージョンでは JSON 形式のみをサポートします。

```json
{
  "prohibited_claims": [
    "drastically",
    "boost productivity",
    "save 90% time"
  ],
  "internal_names": [
    "InternalSystemName",
    "PrivateCodename"
  ]
}
```

## invalid input and output example
以下の内容を含む不正な README.md があるとします：
```markdown
# My Project
This tool will drastically improve your life.
Developed under the project PrivateCodename.
```

スキャンコマンドの実行：
```bash
claim-lint scan README.md
```

出力結果（標準出力）:
```text
ERROR claim.prohibited [line 2]: matched 'drastically' (rule: prohibited_claims) -> Remove unevidenced performance claim.
ERROR internal-name.detected [line 3]: matched 'PrivateCodename' (rule: internal_names) -> Remove internal project name leak.
```
終了コード: 1

## corrected input and success example
修正した README.md：
```markdown
# My Project
This tool is a local-first helper utility.
Developed as a standalone command-line application.
```

スキャンコマンドの実行：
```bash
claim-lint scan README.md
```

出力結果（標準出力）:
```text
No findings.
```
終了コード: 0

## CLI reference
```text
Usage: claim-lint scan <file_path> [options]

Options:
  --config <config_path>  設定ファイル（.claimlintrc.json）のパスを指定します（省略時はカレントディレクトリの .claimlintrc.json を参照）
  --json                  結果を標準出力に JSON 形式で出力します
  -h, --help              ヘルプメッセージを表示します
```

## finding codes
エラー発生時に出力される安定したコードは以下の通りです：
- ERROR claim.prohibited: 設定された prohibited_claims に一致する表現を検出
- ERROR internal-name.detected: 設定された internal_names に一致する表現を検出
- ERROR config.missing: 設定ファイルが見つからない
- ERROR config.invalid: 設定ファイルのパースエラー、または無効な構造

## exit codes
スキャンプロセスの終了時に返される終了コードは以下の通り定義されます：
- 0: 検出されたエラーなし（合格）
- 1: 禁止された主張表現または内部機密用語が検出された（不合格）
- 2: コマンドエラー、ファイル読み込み失敗、または設定ファイルの欠落・破損

## JSON output example
`--json` オプションを指定した場合、以下の構造の JSON が出力されます。

```json
{
  "ok": false,
  "summary": {
    "total_errors": 2
  },
  "findings": [
    {
      "severity": "ERROR",
      "code": "claim.prohibited",
      "line": 2,
      "matched_text": "drastically",
      "rule_source": "prohibited_claims",
      "repair_guidance": "Remove unevidenced performance claim."
    },
    {
      "severity": "ERROR",
      "code": "internal-name.detected",
      "line": 3,
      "matched_text": "PrivateCodename",
      "rule_source": "internal_names",
      "repair_guidance": "Remove internal project name leak."
    }
  ]
}
```

## offline/privacy behavior
claim-lint は外部のネットワーク通信を一切行わない完全オフライン設計です。スキャン処理はすべてローカルマシンのメモリ上で行われ、スキャン対象のファイルデータや設定内容が外部に送信されることはありません。

## relationship to handoff-lint
本ツールは、入力指示書の整合性をスキャンする handoff-lint と対になって動作します。開発フローの開始前に入力を handoff-lint で検査し、開発完了後に公開ドキュメントを claim-lint で検査することで、AI協調開発プロセスの前後にローカルなチェックポイントを設けます。ただし、claim-lint は個人の Markdown リンターとして完全に独立して（standaloneで）動作可能です。

## scope and limitations
- 文字列の決定論的な部分一致（大文字小文字を無視した exact substring matching）のみで動作し、文章の文脈や品質の評価、LLMによる意味的判断は行いません。
- APIキーなどの認証情報（Credentials）はスキャン対象外です。これらには gitleaks 等の専門ツールを使用してください。

## development commands
開発および検証のためのコマンドは以下の通りです：
```bash
python -m pip install -e .[dev]
python -m pytest
```

## license intention
MIT License.
