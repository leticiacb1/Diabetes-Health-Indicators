# Use AWS Lambda's Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Copy the requirements and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip3 install -r requirements.txt

# Copy the application code and model into the image
COPY src/predict.py ${LAMBDA_TASK_ROOT}
COPY models/logistic_regression.pickle ${LAMBDA_TASK_ROOT}

# Command to run the Lambda function
CMD ["predict.run"]