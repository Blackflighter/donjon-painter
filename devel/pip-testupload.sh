#!/bin/bash

version=0.9.5

twine upload --repository-url https://test.pypi.org/legacy/ ../dist/donjon_painter-$version-py3-none-any.whl ../dist/donjon-painter-$version.tar.gz
