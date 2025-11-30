from pathlib import Path

from bs4 import BeautifulSoup
from typer.testing import CliRunner

from nprompter.__main__ import app

runner = CliRunner()


def test_app(tmp_path: Path):
    result = runner.invoke(app, ["build", "c68ccc052d1b4eaaa3091e637f7011c0", "--output", tmp_path])
    assert result.exit_code == 0, result.output
    assert (tmp_path / "index.html").exists()
    with open(tmp_path / "index.html", "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        assert soup.find("h2").text == "Example board"
        pages = soup.find("ul").find_all("li")
        assert len(pages) == 7
