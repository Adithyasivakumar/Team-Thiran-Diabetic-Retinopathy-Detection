from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from decouple import config
import os
import time

#--------------------------------------------------------
# Twilio SMS Configuration
# Credentials loaded from .env file for security
#-------------------------------------------------------

# Twilio error codes and meanings
TWILIO_ERROR_CODES = {
    21608: "Cannot send SMS to unverified recipient (trial account)",
    21614: "API key/auth token error",
    20003: "Account suspended or trial account timeout",
    21201: "Invalid 'To' phone number",
    21211: "Invalid 'From' phone number",
    30001: "Queue overflow - too many messages",
    30002: "Account suspended",
    30003: "Unreachable destination handset",
    30004: "Message blocked by carrier",
    30005: "Unknown destination handset",
    30006: "Landline or unreachable carrier",
    30007: "Carrier violation",
    30008: "Unknown error",
    30044: "US number cannot send international SMS - need local number for destination country",
}

def send(value, classes):
    """
    Send SMS notification with DR prediction results
    (Legacy function - kept for backward compatibility)
    
    Args:
        value: Prediction severity level (0-4)
        classes: Prediction class name (e.g., "No DR", "Moderate")
    """
    try:
        # Load credentials from .env file
        account_sid = config('TWILIO_ACCOUNT_SID', default=os.getenv('TWILIO_ACCOUNT_SID'))
        auth_token = config('TWILIO_AUTH_TOKEN', default=os.getenv('TWILIO_AUTH_TOKEN'))
        from_phone = config('TWILIO_PHONE', default=os.getenv('TWILIO_PHONE'))
        to_phone = config('RECIPIENT_PHONE', default=os.getenv('RECIPIENT_PHONE'))
        
        if not all([account_sid, auth_token, from_phone, to_phone]):
            print("❌ Error: Missing Twilio credentials in .env file")
            return None
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Format phone number for Indian numbers
        if to_phone.startswith('9') and len(to_phone) == 10:
            to_phone = f"+91{to_phone}"
        
        # Create and send message
        message = client.messages.create(
            to=to_phone,
            from_=from_phone,
            body=f"Team Thiran - DR Detection Report\n\nSeverity Level: {value}\nClassification: {classes}\n\nPlease consult an ophthalmologist for confirmation."
        )
        
        print('✅ Message sent successfully!')
        print(f'Message SID: {message.sid}')
        return message.sid
        
    except Exception as e:
        print(f"❌ SMS Error: {str(e)}")
        return None


def _normalize_phone(phone_number):
    if not phone_number:
        return phone_number

    cleaned = ''.join(ch for ch in phone_number.strip() if ch.isdigit() or ch == '+')
    if cleaned.startswith('+'):
        digits = '+' + ''.join(ch for ch in cleaned if ch.isdigit())
    else:
        digits = ''.join(ch for ch in cleaned if ch.isdigit())

    if digits.startswith('+'):
        return digits
    if digits.startswith('91') and len(digits) == 12:
        return '+' + digits
    if len(digits) == 10:
        default_cc = os.getenv('DEFAULT_COUNTRY_CODE', '91').lstrip('+')
        return f'+{default_cc}{digits}'
    return digits


def check_message_status(message_sid):
    """
    Check the delivery status of a sent message with detailed diagnostics
    
    Args:
        message_sid: Twilio Message SID
    
    Returns:
        dict: Detailed status information or None
    """
    try:
        account_sid = config('TWILIO_ACCOUNT_SID', default=os.getenv('TWILIO_ACCOUNT_SID'))
        auth_token = config('TWILIO_AUTH_TOKEN', default=os.getenv('TWILIO_AUTH_TOKEN'))
        
        if not account_sid or not auth_token:
            return None
        
        client = Client(account_sid, auth_token)
        message = client.messages(message_sid).fetch()
        
        # Extract all available information
        error_code = message.error_code
        error_msg = message.error_message or "No error message from Twilio"
        
        # Interpret error code
        error_hint = TWILIO_ERROR_CODES.get(error_code, "Unknown error")
        
        return {
            'status': message.status,
            'to': message.to,
            'from': message.from_,
            'error_code': error_code,
            'error_message': error_msg,
            'error_hint': error_hint,
            'date_sent': message.date_sent,
            'price': message.price
        }
    except Exception as e:
        print(f"❌ Error checking message status: {e}")
        return None


def diagnose_twilio_connection():
    """
    Test Twilio credentials and connection
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_phone = os.getenv('TWILIO_PHONE')
        
        if not account_sid:
            return (False, "TWILIO_ACCOUNT_SID not set in .env")
        if not auth_token:
            return (False, "TWILIO_AUTH_TOKEN not set in .env")
        if not from_phone:
            return (False, "TWILIO_PHONE not set in .env")
        
        # Try to create client
        client = Client(account_sid, auth_token)
        
        # Verify by fetching account details
        account = client.api.accounts(account_sid).fetch()
        
        return (True, f"✅ Twilio connection OK. Account: {account.friendly_name}, Status: {account.status}")
    except TwilioRestException as e:
        return (False, f"Twilio API error {e.code}: {e.msg}")
    except Exception as e:
        return (False, f"Connection error: {str(e)}")


def send_report_sms(patient_phone, report_summary, return_error=False):
    """
    Send medical report via SMS with comprehensive error handling
    
    Args:
        patient_phone: Patient's phone number
        report_summary: Formatted report summary text
        return_error: If True, returns tuple (sid, error_msg)
    
    Returns:
        str: Message SID on success, None on failure
        tuple: (sid, error_msg) if return_error=True
    """
    try:
        # Get credentials
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_phone = os.getenv('TWILIO_PHONE')
        messaging_service_sid = os.getenv('TWILIO_MESSAGING_SERVICE_SID')
        
        print("\n" + "="*60)
        print("TWILIO SMS SENDING DIAGNOSTIC")
        print("="*60)
        
        # Validate credentials exist
        print("\n1️⃣  Checking credentials...")
        if not account_sid:
            err = "TWILIO_ACCOUNT_SID not set in .env"
            print(f"❌ {err}")
            return (None, err) if return_error else None
        
        if not auth_token:
            err = "TWILIO_AUTH_TOKEN not set in .env"
            print(f"❌ {err}")
            return (None, err) if return_error else None
        
        if not from_phone and not messaging_service_sid:
            err = "Neither TWILIO_PHONE nor TWILIO_MESSAGING_SERVICE_SID is set"
            print(f"❌ {err}")
            return (None, err) if return_error else None
        
        print("✅ Credentials found")
        
        # Verify Twilio connection
        print("\n2️⃣  Verifying Twilio connection...")
        success, msg = diagnose_twilio_connection()
        print(msg)
        if not success:
            return (None, msg) if return_error else None
        
        # Normalize phone numbers
        print("\n3️⃣  Normalizing phone numbers...")
        original_phone = patient_phone
        patient_phone = _normalize_phone(patient_phone)
        from_phone_normalized = _normalize_phone(from_phone) if from_phone else None
        
        print(f"   Patient phone: {original_phone} → {patient_phone}")
        if from_phone_normalized:
            print(f"   From phone:    {from_phone} → {from_phone_normalized}")
        
        # Create Twilio client
        print("\n4️⃣  Creating Twilio client...")
        client = Client(account_sid, auth_token)
        print("✅ Client created")
        
        # Send message
        print("\n5️⃣  Sending SMS...")
        message_kwargs = {
            "to": patient_phone,
            "body": report_summary
        }
        
        if messaging_service_sid:
            message_kwargs["messaging_service_sid"] = messaging_service_sid
            print(f"   Using Messaging Service SID: {messaging_service_sid[:10]}...")
        else:
            message_kwargs["from_"] = from_phone_normalized
            print(f"   Using from phone: {from_phone_normalized}")
        
        message = client.messages.create(**message_kwargs)
        print(f"✅ SMS accepted by Twilio")
        print(f"   Message SID: {message.sid}")
        print(f"   Initial Status: {message.status}")
        
        # Wait and check delivery status
        print("\n6️⃣  Checking delivery status (waiting 3 seconds)...")
        time.sleep(3)
        
        status_info = check_message_status(message.sid)
        
        if not status_info:
            err = "Could not fetch message status"
            print(f"❌ {err}")
            return (None, err) if return_error else None
        
        status = status_info['status']
        error_code = status_info['error_code']
        error_message = status_info['error_message']
        error_hint = status_info['error_hint']
        
        print(f"\n   Status: {status}")
        print(f"   To: {status_info['to']}")
        print(f"   From: {status_info['from']}")
        
        if error_code:
            print(f"   Error Code: {error_code}")
            print(f"   Error Message: {error_message}")
            print(f"   ℹ️  Hint: {error_hint}")
        
        print("\n" + "="*60)
        
        # Handle different statuses
        if status == 'delivered':
            print("✅ SMS DELIVERED SUCCESSFULLY!")
            print("="*60 + "\n")
            return (message.sid, None) if return_error else message.sid
        
        elif status == 'sent':
            print("📨 SMS sent - waiting for delivery")
            print("="*60 + "\n")
            return (message.sid, None) if return_error else message.sid
        
        elif status == 'queued':
            print("⏳ SMS queued - delivery pending")
            print("="*60 + "\n")
            return (message.sid, None) if return_error else message.sid
        
        elif status == 'failed':
            if error_code == 21608:
                err = f"❌ RECIPIENT NOT VERIFIED (Error 21608)\n\nOn Twilio trial accounts, you must verify the recipient number.\nVerified numbers:\n  • +91 95444 15691\n  • +91 90438 90506\n\nPlease verify the target number in Twilio Console."
            elif error_code:
                err = f"❌ SMS Delivery Failed\nError {error_code}: {error_message}\nHint: {error_hint}"
            else:
                err = f"❌ SMS Delivery Failed without specific error\nMessage: {error_message}"
            
            print(err)
            print("="*60 + "\n")
            return (None, err) if return_error else None
        
        elif status == 'undelivered':
            err = f"❌ SMS Undelivered after multiple attempts\nError: {error_message}"
            print(err)
            print("="*60 + "\n")
            return (None, err) if return_error else None
        
        else:
            err = f"⚠️  Unknown status: {status}"
            print(err)
            print("="*60 + "\n")
            return (None, err) if return_error else None
    
    except TwilioRestException as e:
        error_detail = f"Twilio API Error {e.code}: {e.msg}"
        print(f"\n❌ {error_detail}")
        
        if e.code == 21608:
            error_detail = "Recipient number not verified. Please verify in Twilio Console."
        elif e.code == 21201:
            error_detail = "Invalid recipient phone number format"
        elif e.code == 21211:
            error_detail = "Invalid sender (TWILIO_PHONE) phone number format"
        elif e.code == 20003:
            error_detail = "Account suspended or trial account timeout"
        
        print("="*60 + "\n")
        return (None, error_detail) if return_error else None
    
    except Exception as e:
        error_detail = f"Unexpected error: {str(e)}"
        print(f"\n❌ {error_detail}")
        print("="*60 + "\n")
        return (None, error_detail) if return_error else None


