import pyotp
from datetime import datetime, timedelta

def send_otp(request):
    # One time password
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)

    otp = totp.now()

    request.session['otp_secret_key'] = totp.secret

    valid_date = datetime.now() + timedelta(minutes=1)

    request.session['otp_valid_date'] = str(valid_date)
    print(f"Your one time password is :{otp}")

def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'