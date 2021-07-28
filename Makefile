all: install

install:
	virtualenv .env --python=python3.6
	.env/bin/python -m pip install -U setuptools
	.env/bin/python -m pip install --upgrade pip
	.env/bin/python -m pip install -r requirements.txt
	.env/bin/python -m pip install ipykernel
	.env/bin/python -m ipykernel install --name=.env
	npm install -g serverless
	serverless plugin install -n serverless-python-requirements
	# serverless plugin install -n serverless-add-api-key
	serverless plugin install -n serverless-plugin-warmup
	serverless plugin install -n serverless-appsync-plugin
	serverless plugin install -n serverless-dynamodb-autoscaling

clean:
	rm -rf .env/

deploy:
	serverless deploy -v
