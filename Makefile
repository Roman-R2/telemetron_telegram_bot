code-check:
	isort services/ settings/ launcher.py
	flake8 --extend-ignore E501 services/ settings/ launcher.py