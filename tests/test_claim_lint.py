import os
import json
import pytest
import sys
from unittest.mock import patch
from claim_lint.cli import main
from claim_lint.config import load_config, ConfigError

# テスト用の設定ファイル作成ヘルパー
def create_config(path, prohibited=None, internal=None):
    if prohibited is None:
        prohibited = ["drastically", "boost productivity", "save 90% time"]
    if internal is None:
        internal = ["InternalSystemName", "PrivateCodename"]
    
    data = {
        "prohibited_claims": prohibited,
        "internal_names": internal
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

# テスト用のスキャン対象ファイル作成ヘルパー
def create_target_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# 1. ヘルプメッセージの正常出力確認
def test_cli_help(capsys):
    testargs = ["claim-lint", "-h"]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "show this help message and exit" in captured.out

# 2. 該当項目がない場合に成功（exit 0）すること
def test_scan_no_findings(tmp_path, capsys):
    cfg_path = tmp_path / ".claimlintrc.json"
    target_path = tmp_path / "README.md"
    create_config(cfg_path)
    create_target_file(target_path, "# Project\nThis is a local helper utility.\nIt runs standalone.")

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(cfg_path)]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "No findings." in captured.out

# 3. 禁止表現が含まれる行を正しく検出し exit 1 となること
def test_scan_prohibited_claim(tmp_path, capsys):
    cfg_path = tmp_path / ".claimlintrc.json"
    target_path = tmp_path / "README.md"
    create_config(cfg_path)
    create_target_file(target_path, "# Project\nThis tool will drastically improve life.\nSafe to run.")

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(cfg_path)]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "ERROR claim.prohibited [line 2]: matched 'drastically'" in captured.out

# 4. 機密用語が含まれる行を正しく検出し exit 1 となること
def test_scan_internal_name(tmp_path, capsys):
    cfg_path = tmp_path / ".claimlintrc.json"
    target_path = tmp_path / "README.md"
    create_config(cfg_path)
    create_target_file(target_path, "# Project\nRuns on PrivateCodename platform.\nDone.")

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(cfg_path)]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "ERROR internal-name.detected [line 2]: matched 'PrivateCodename'" in captured.out

# 5. 複数行のエラーをまとめて検出できること
def test_scan_multiple_errors(tmp_path, capsys):
    cfg_path = tmp_path / ".claimlintrc.json"
    target_path = tmp_path / "README.md"
    create_config(cfg_path)
    create_target_file(target_path, "# Project\nThis will drastically save 90% time.\nUsing InternalSystemName here.")

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(cfg_path)]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 1
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) >= 3 # drastically, save 90% time on line 2, and InternalSystemName on line 3

# 6. --json オプション時に正しいスキーマの JSON が出力されること
def test_scan_json_output(tmp_path, capsys):
    cfg_path = tmp_path / ".claimlintrc.json"
    target_path = tmp_path / "README.md"
    create_config(cfg_path)
    create_target_file(target_path, "# Project\nContains drastically and PrivateCodename.")

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(cfg_path), "--json"]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 1
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["ok"] is False
    assert data["summary"]["total_errors"] == 2
    assert len(data["findings"]) == 2
    assert data["findings"][0]["code"] == "claim.prohibited"
    assert data["findings"][1]["code"] == "internal-name.detected"

# 7. 大文字小文字が異なる場合でもマッチングが行われること
def test_scan_case_insensitivity(tmp_path, capsys):
    cfg_path = tmp_path / ".claimlintrc.json"
    target_path = tmp_path / "README.md"
    create_config(cfg_path, prohibited=["DrAsTiCaLlY"], internal=["privatecodename"])
    create_target_file(target_path, "Uses DRASTICALLY and PrivateCodename.")

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(cfg_path)]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "drastically" in captured.out.lower()
    assert "privatecodename" in captured.out.lower()

# 8. デフォルト設定ファイルがない場合に config.missing エラー（exit 2）を出すこと
def test_config_missing_default(tmp_path, capsys):
    # カレントディレクトリを一時ディレクトリに移動させてテスト
    old_cwd = os.getcwd()
    os.chdir(str(tmp_path))
    target_path = tmp_path / "README.md"
    create_target_file(target_path, "Some content.")

    testargs = ["claim-lint", "scan", str(target_path)]
    try:
        with patch.object(sys, "argv", testargs):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 2
        captured = capsys.readouterr()
        assert "ERROR config.missing" in captured.err
    finally:
        os.chdir(old_cwd)

# 9. 指定されたカスタム設定ファイルがない場合に config.missing エラー（exit 2）を出すこと
def test_config_missing_custom(tmp_path, capsys):
    target_path = tmp_path / "README.md"
    create_target_file(target_path, "Some content.")
    non_exist_cfg = tmp_path / "non_exist.json"

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(non_exist_cfg)]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert "ERROR config.missing" in captured.err

# 10. 設定ファイルが不正なJSONの場合に config.invalid エラー（exit 2）を出すこと
def test_config_invalid_json(tmp_path, capsys):
    cfg_path = tmp_path / ".claimlintrc.json"
    target_path = tmp_path / "README.md"
    create_target_file(target_path, "Some content.")
    with open(cfg_path, "w") as f:
        f.write("{ invalid json")

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(cfg_path)]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert "ERROR config.invalid" in captured.err

# 11. 設定ファイルのキー構成が無効な場合に config.invalid エラー（exit 2）を出すこと
def test_config_invalid_schema(tmp_path, capsys):
    cfg_path = tmp_path / ".claimlintrc.json"
    target_path = tmp_path / "README.md"
    create_target_file(target_path, "Some content.")
    
    # 必須キーが足りない
    with open(cfg_path, "w") as f:
        json.dump({"prohibited_claims": []}, f)

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(cfg_path)]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert "ERROR config.invalid" in captured.err

# 12. 走査対象ファイルが存在しない場合に exit 2 となること
def test_file_unreadable(tmp_path, capsys):
    cfg_path = tmp_path / ".claimlintrc.json"
    create_config(cfg_path)
    non_exist_target = tmp_path / "non_exist.md"

    testargs = ["claim-lint", "scan", str(non_exist_target), "--config", str(cfg_path)]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert "ERROR file.missing" in captured.err

# 13. 複数行あるファイルの正しい行番号が検出されること
def test_line_number_correctness(tmp_path, capsys):
    cfg_path = tmp_path / ".claimlintrc.json"
    target_path = tmp_path / "README.md"
    create_config(cfg_path)
    
    content = "\n\n\nThis line has drastically claim.\n\nAnd PrivateCodename is here."
    create_target_file(target_path, content)

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(cfg_path)]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 1
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert "line 4" in lines[0]
    assert "line 6" in lines[1]

# 14. 設定ファイルのリストが空の場合に何もマッチせず正常終了すること
def test_empty_rules_pass(tmp_path, capsys):
    cfg_path = tmp_path / ".claimlintrc.json"
    target_path = tmp_path / "README.md"
    create_config(cfg_path, prohibited=[], internal=[])
    create_target_file(target_path, "Contains drastically and PrivateCodename.")

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(cfg_path)]
    with patch.object(sys, "argv", testargs):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "No findings." in captured.out

# 15. handoff-lint がインストールされていない環境でも正しく単独動作すること
def test_standalone_behavior(tmp_path, capsys):
    # インポート可能なモジュールとして handoff_lint がない状態をシミュレート
    # 単に本パッケージ自身を実行することで、外部のモジュールに依存せずスタンドアロンで動くことを確認
    cfg_path = tmp_path / ".claimlintrc.json"
    target_path = tmp_path / "README.md"
    create_config(cfg_path)
    create_target_file(target_path, "# Hello")

    testargs = ["claim-lint", "scan", str(target_path), "--config", str(cfg_path)]
    with patch.object(sys, "argv", testargs):
        with patch.dict("sys.modules", {"handoff_lint": None}):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "No findings." in captured.out
