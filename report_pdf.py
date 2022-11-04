import requests
import pdfkit
import os 

#host and end point to generate email allure report
host = "http://localhost:5050/allure-docker-service"
endpoint = "/emailable-report/export?project_id="
project_name = "android"

#host and endpoint for sending report to slack 
host_slack = "https://slack.com"
end_point_slack_upload = "/api/files.upload"
token_slack_upload = ""
channels = ""

def generate_pdf_report():
    global host
    global endpoint
    global project_name
    full_url_request = host + endpoint + project_name
    response = requests.get(full_url_request)
    response_body = response.text
    #f = open ("report.html", "w")
    #f.write(response_body)
    #f.close()
    path_report_pdf = os.getcwd()+"/report.pdf"
    pdfkit.from_string(response_body, path_report_pdf)
    send_to_slack_notif(path_report_pdf)

def send_to_slack_notif(pdf_name):
    global host_slack
    global end_point_slack_upload
    global token_slack_upload
    global channels
    full_url_upload_slack = host_slack + end_point_slack_upload
    print(pdf_name)
    

    file = {
        "file": open(pdf_name, 'rb')
    }

    form_data = {
        "channels": channels,
        "token": token_slack_upload,
        "initial_comment": "Test Upload",
    }

    response = requests.post(full_url_upload_slack, data=form_data, files=file)
    print(str(response.status_code)+" : "+response.text)

if __name__ == "__main__":
    generate_pdf_report()