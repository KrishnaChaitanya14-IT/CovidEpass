import requests
from flask import Flask, render_template, request
from twilio.rest import Client

account_sid = 'ACd8815af9da35549205d0c70d42b192a0'
auth_token = '2feae9eb3b9c7a57ee4cc05fe49cfb7e'
client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def registration_form():
    return render_template('test_page.html')


@app.route('/user_registration_dtls', methods=['GET', 'POST'])
def login_registration_dtls():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['dest_state']
    destination_dt = request.form['destination']
    phoneNumber = request.form['phoneNumber']
    date = request.form['travel']
    id_proof = request.form['idcard']
    full_name = first_name + "." + last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt / pop) * 100)
    if travel_pass < 30 and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(to=phoneNumber,
                               from_="+13474620289",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " + source_dt + " to " +
                                    destination_dt + " " + "on"+ date +"Has " + " " + status)
        return render_template('user_registration_dtls.html', firstname=first_name, lastname=last_name,
                               status="confirmed", email=email_id, fro= source_dt, to = destination_dt, phNo=phoneNumber, idproof=id_proof,Date=date)
    else:
        status = 'NOT CONFIRMED'
        client.messages.create(to=phoneNumber,
                               from_="+13474620289",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " +
                                    source_dt + " to " + destination_dt + " " + "Has " + " " + status + " " +
                                    ", Apply later")
        return render_template('user_registration_dtls.html', firstname=first_name, lastname=last_name,
                               status="confirmed", email=email_id,fro=source_dt,to = destination_dt,phNo=phoneNumber,idproof=id_proof)


if __name__ == "__main__":
    app.run(port=9001, debug=True)
