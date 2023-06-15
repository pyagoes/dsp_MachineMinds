import os
import great_expectations as gx
from great_expectations.data_context import FileDataContext
import pytz
import shutil
import json
import requests
import psycopg2
from psycopg2 import Error

# Initialize a filesystem data context
relative_folderA_path = "./data_validation/"
relative_folderB_path = "./bad_quality_data/"
relative_folderC_path = "./good_quality_data/"

absolute_folderA_path = os.path.abspath(relative_folderA_path)
absolute_folderB_path = os.path.abspath(relative_folderB_path)
absolute_folderC_path = os.path.abspath(relative_folderC_path)

context = FileDataContext.create(project_root_dir=absolute_folderA_path)

# Create the connection to the db
try:
    connection = psycopg2.connect(
        user="MachineMinds",
        password="MachineMinds",
        host="localhost",
        port="5432",
        database="customer_churn"
    )
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL:", error)



# Create expectation suite
expectation_suite_name = "telco_churn_suite"
if expectation_suite_name not in context.list_expectation_suite_names():
    context.create_expectation_suite(expectation_suite_name)

# Create a data source & asset
datasource_name = "folderA"
asset_name = "telco_churn_data"
batching_regex = r".*\.csv"
for element in context.list_datasources():
    if datasource_name != element["name"]:
        datasource = context.sources.add_pandas_filesystem(name=datasource_name, base_directory=relative_folderA_path)
        datasource.add_csv_asset(name=asset_name, batching_regex=batching_regex)
    else:   
    # Create a batch request
        data_asset = context.get_datasource(datasource_name).get_asset(asset_name)
        batch_request = data_asset.build_batch_request()
        
data_asset = context.get_datasource(datasource_name).get_asset(asset_name)
batch_request = data_asset.build_batch_request()

# Create a validator and save the desired expectations to a suite
validator = context.get_validator(batch_request=batch_request, expectation_suite_name="telco_churn_suite")
existing_expectations = validator.get_expectation_suite().expectations
if not existing_expectations: 
    validator.expect_table_column_count_to_equal(20)

    columns_list = ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService",
                    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
                    "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
                    "MonthlyCharges", "TotalCharges"]
    for column_name in columns_list:
        validator.expect_column_to_exist(column=column_name)

    validator.expect_column_values_to_not_be_null(column="SeniorCitizen")
    validator.expect_column_values_to_not_be_null(column="tenure")
    validator.expect_column_values_to_not_be_null(column="MonthlyCharges")
    validator.expect_column_values_to_not_be_null(column="TotalCharges")

    validator.expect_column_distinct_values_to_be_in_set(column="SeniorCitizen", value_set=[0, 1])

    validator.save_expectation_suite(discard_failed_expectations=False)

 # Create a checkpoint
checkpoint = gx.checkpoint.SimpleCheckpoint(
    name="telco_churn_checkpoint",
    data_context=context,
    validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": "telco_churn_suite",
        },
        
    ],
)

checkpoint = context.get_checkpoint("telco_churn_checkpoint")
checkpoint_result = checkpoint.run()
context.build_data_docs()

# Initialize an alert on teams:
def send_teams_alert(webhook_url, message):
    # Create the payload
    payload = {
        "text": message
    }

    # Send the HTTP POST request to the webhook URL
    response = requests.post(webhook_url, json.dumps(payload))

    # Check the response status code
    if response.status_code != 200:
        print(f"Error sending Microsoft Teams alert. Status code: {response.status_code}")
    else:
        print("Microsoft Teams alert sent successfully.")

print(checkpoint_result)
# Parse the checkpoint run
overall_result = checkpoint_result.success
checkpoint_time = checkpoint_result.run_id.run_time
exception_results = checkpoint_result.run_results
exception_results_key = list(exception_results.keys())[0]
file_name = exception_results[exception_results_key]["validation_result"]["meta"]["active_batch_definition"]["batch_identifiers"]["path"]

if overall_result == True:
    # Move the file to good_quality_folder
    shutil.move(absolute_folderA_path+ "/" + file_name, absolute_folderC_path)
    print("the file was moved to good_quality_data folder")
else:
    # Move the file to bad_quality_data folder
    shutil.move(absolute_folderA_path+ "/" + file_name, absolute_folderB_path)
    print("the file was moved to bad_quality_data folder")

    #send an alert on teams
    webhook_url = "https://epitafr.webhook.office.com/webhookb2/bbdb532c-1292-40ef-8d50-44b7bfc35055@3534b3d7-316c-4bc9-9ede-605c860f49d2/IncomingWebhook/2b057e73ef6b47daa57b40ac0d380765/87f53d74-42d9-4b75-8543-1c1966577f7a"
    message = "Hi MachineMinds! \U0001F603 	" + "There is a quality validation issue with the last uploaded file \U0001F631	" + "Usually this is bad news but for the sake of your project this is gooood \U0001F973"
    send_teams_alert(webhook_url, message)

    # Extract data / save data into db 
    parsing_list = []
    for element in exception_results[exception_results_key]["validation_result"]["results"]:
        element_result = element["success"]
        element_type = element["expectation_config"]["expectation_type"]
        try:
            element_column = element["expectation_config"]["kwargs"]["column"]
        except:
            element_column = "zero_arg"
        parsing_list += [[element_result, element_column, element_type]]

    sorted_parsing_list = sorted(parsing_list, key=lambda x: x[1])
    file_name = file_name
    paris_timezone = pytz.timezone('Europe/Paris')
    execution_time = checkpoint_time.astimezone(paris_timezone)
    expected_columns_count = sorted_parsing_list[25][0]
    customer_id_expected = sorted_parsing_list[21][0]
    gender_expected = sorted_parsing_list[22][0]
    senior_citizen_expected = sorted_parsing_list[13][0]
    partner_expected = sorted_parsing_list[10][0]
    dependent_expected = sorted_parsing_list[1][0]
    tenure_expected = sorted_parsing_list[23][0]
    phone_service_expected = sorted_parsing_list[12][0]
    multiple_lines_expected = sorted_parsing_list[6][0]
    internet_service_expected = sorted_parsing_list[3][0]
    online_security_expected = sorted_parsing_list[8][0]
    online_backup_expected = sorted_parsing_list[7][0]
    device_protection_expected = sorted_parsing_list[2][0]
    tech_support_expected = sorted_parsing_list[18][0]
    streaming_tv_expected = sorted_parsing_list[17][0]
    streaming_movies_expected = sorted_parsing_list[16][0]
    contract_expected = sorted_parsing_list[0][0]
    paperless_billing_expected = sorted_parsing_list[9][0]
    payment_method_expected = sorted_parsing_list[11][0]
    monthly_charges_expected = sorted_parsing_list[4][0]
    total_charges_expected = sorted_parsing_list[19][0]
    senior_citizen_notnull = sorted_parsing_list[14][0]
    tenure_notnull = sorted_parsing_list[24][0]
    monthly_charges_notnull = sorted_parsing_list[5][0]
    total_charges_notnull = sorted_parsing_list[20][0]
    senior_citizen_values_expected = sorted_parsing_list[15][0]

    final_result = {"file_name": file_name, "execution_time": execution_time, "expected_columns_count": expected_columns_count,
                    "customer_id_expected": customer_id_expected, "gender_expected": gender_expected, "senior_citizen_expected": senior_citizen_expected,
                    "partner_expected": partner_expected, "dependent_expected": dependent_expected, "tenure_expected": tenure_expected,
                    "phone_service_expected": phone_service_expected, "multiple_lines_expected": multiple_lines_expected, "internet_service_expected": internet_service_expected,
                    "online_security_expected": online_security_expected, "online_backup_expected": online_backup_expected, "device_protection_expected": device_protection_expected,
                    "tech_support_expected": tech_support_expected, "streaming_tv_expected": streaming_tv_expected, "streaming_movies_expected": streaming_movies_expected,
                    "contract_expected": contract_expected, "paperless_billing_expected": paperless_billing_expected, "payment_method_expected": payment_method_expected,
                    "monthly_charges_expected": monthly_charges_expected, "total_charges_expected": total_charges_expected, "senior_citizen_notnull": senior_citizen_notnull,
                    "tenure_notnull": tenure_notnull, "monthly_charges_notnull": monthly_charges_notnull, "total_charges_notnull": total_charges_notnull,
                    "senior_citizen_values_expected": senior_citizen_values_expected}

    # Save the results to the db
    cursor = connection.cursor()

    sql_insert = """INSERT INTO data_quality (
    file_name, execution_time, expected_columns_count, customer_id_expected, gender_expected, senior_citizen_expected,
    partner_expected, dependent_expected, tenure_expected, phone_service_expected, multiple_lines_expected,
    internet_service_expected, online_security_expected, online_backup_expected, device_protection_expected,
    tech_support_expected, streaming_tv_expected, streaming_movies_expected, contract_expected,
    paperless_billing_expected, payment_method_expected, monthly_charges_expected, total_charges_expected,
    senior_citizen_notnull, tenure_notnull, monthly_charges_notnull, total_charges_notnull,
    senior_citizen_values_expected) VALUES (%(file_name)s, %(execution_time)s, %(expected_columns_count)s, %(customer_id_expected)s, %(gender_expected)s, %(senior_citizen_expected)s,
    %(partner_expected)s, %(dependent_expected)s, %(tenure_expected)s, %(phone_service_expected)s, %(multiple_lines_expected)s,
    %(internet_service_expected)s, %(online_security_expected)s, %(online_backup_expected)s, %(device_protection_expected)s,
    %(tech_support_expected)s, %(streaming_tv_expected)s, %(streaming_movies_expected)s, %(contract_expected)s,
    %(paperless_billing_expected)s, %(payment_method_expected)s, %(monthly_charges_expected)s, %(total_charges_expected)s,
    %(senior_citizen_notnull)s, %(tenure_notnull)s, %(monthly_charges_notnull)s, %(total_charges_notnull)s,
    %(senior_citizen_values_expected)s)"""

    cursor.execute(sql_insert, final_result)
    connection.commit()
    cursor.close()
    connection.close()

