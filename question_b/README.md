# Version Compare

Version Compare is a Python library to compare version strings.

## Installation

You can install the library using `pip`:

```bash
pip install version_compare
```

## Usage
``` python
from version_compare import compare_versions

result = compare_versions("1.2", "1.1")
print(result)  # Output: 1
```
## Tests
The tests can be run with 
``` bash
python -m unittest discover -s tests
```