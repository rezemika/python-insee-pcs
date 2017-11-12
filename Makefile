freeze:
	pip3 freeze | grep -v "pkg-resources" > requirements.txt

tests:
	python3 insee_pcs/test_main.py
