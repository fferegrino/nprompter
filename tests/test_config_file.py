import pytest

from nprompter.cli.helpers import get_config


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
