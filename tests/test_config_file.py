import tomllib
from pathlib import Path

import pytest
from typer.testing import CliRunner

from nprompter.__main__ import app
from nprompter.cli.defaults import DEFAULT_CONFIG_PATH
from nprompter.cli.helpers import get_config

runner = CliRunner()


@pytest.fixture
def in_temporary_dir(tmpdir):
    with tmpdir.as_cwd():
        yield tmpdir


def test_non_existent_config(in_temporary_dir):
    config = get_config("local.toml")
    assert config


def test_reads_file(in_temporary_dir):
    config_file = in_temporary_dir / "local.toml"
    with open(config_file, "w") as writable:
        writable.write(
            """[font]
size = 1000
        """
        )

    config = get_config(str(config_file))

    assert config["font"]["size"] == 1000


def test_applies_defaults(in_temporary_dir):
    config_file = in_temporary_dir / "local.toml"
    with open(config_file, "w") as writable:
        writable.write(
            """[font]
size = 1000
        """
        )

    config = get_config(str(config_file))

    assert config["font"]["line_height_increment"] == 0.1
    assert config["font"]["size"] == 1000


def test_create_config_command(in_temporary_dir):
    result = runner.invoke(app, ["create-config"])
    assert result.exit_code == 0
    config_file = Path(DEFAULT_CONFIG_PATH)
    assert config_file.exists()
    content = config_file.read_bytes()
    parsed = tomllib.loads(content.decode("utf-8"))
    assert "font" in parsed
    assert "screen" in parsed


def test_create_config_already_exists_without_override(in_temporary_dir):
    Path(DEFAULT_CONFIG_PATH).write_text("dummy = true", encoding="utf-8")
    result = runner.invoke(app, ["create-config"])
    assert result.exit_code == 1
    assert "already exists" in result.output


def test_create_config_override(in_temporary_dir):
    Path(DEFAULT_CONFIG_PATH).write_text("dummy = true", encoding="utf-8")
    result = runner.invoke(app, ["create-config", "--override"])
    assert result.exit_code == 0
    parsed = tomllib.loads(Path(DEFAULT_CONFIG_PATH).read_text(encoding="utf-8"))
    assert "font" in parsed
    assert "dummy" not in parsed


def test_build_with_invalid_toml(in_temporary_dir):
    bad_config = Path("bad.toml")
    bad_config.write_text("invalid = [toml unclosed", encoding="utf-8")
    result = runner.invoke(app, ["build", "dummy_db", "--config", str(bad_config)])
    assert result.exit_code == 1
    assert "invalid TOML syntax" in result.output
