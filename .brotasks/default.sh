#!/bin/sh

setup() {
	pyenv virtualenv 3.4.3 webpreview
	pyenv activate webpreview
	pip install --upgrade pip
	pip install -r requirements.txt
}

init() {
	pyenv activate
	echo "Happy hacking !!!"
}

publish() {
	python setup.py bdist_wheel
	twine upload dist/*
}

$@
