import toml

def test_version():

    from actymath import __version__

    # Read the pyproject.toml file
    with open("pyproject.toml", "r") as f:
        pyproject_toml = toml.load(f)

    # Check the version in the pyproject.toml file matches the __version__ in __init__.py
    pyproject_toml_version = pyproject_toml["tool"]["poetry"]["version"]

    assert pyproject_toml_version == __version__
