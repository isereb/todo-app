# TODO app

This is a simple Flask RestAPI in Python for creating TODOs. 

* Hosted on **AWS**
* To be ran as a *serverless* app
* Uses *DynamoDB* for storage

## Getting started

#### Deploy in your own AWS account
```
sam deploy --guided
```

#### Run locally
1. Uncomment the following line
```python
app.run(host="127.0.0.1", port=8000, debug=True)
```
2. Make sure DynamoDB table exists: `${AWS_STACK_NAME}-table`
3. then run main.py
```bash
pip3 install -r requirements.txt
python3 main.py
```