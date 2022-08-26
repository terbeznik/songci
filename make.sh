#!/bin/bash
rm -r dist
rm -r build
rm -r *.egg-info
python3 setup.py sdist
twine upload dist/*