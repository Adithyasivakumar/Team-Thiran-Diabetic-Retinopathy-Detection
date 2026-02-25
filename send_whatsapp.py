"""
WhatsApp Integration for Medical Report Delivery
Sends formatted medical reports with PDF attachments via WhatsApp
Uses Twilio WhatsApp API
"""

from twilio.rest import Client
from decouple import config
import os

class WhatsAppReportSender:
    """Send medical reports via WhatsApp with PDF attachments"""
    
    def __init__(self):
        """Initialize Twilio client for WhatsApp"""
        self.account_sid = config('TWILIO_ACCOUNT_SID', default=os.getenv('TWILIO_ACCOUNT_SID'))
        self.auth_token = config('TWILIO_AUTH_TOKEN', default=os.getenv('TWILIO_AUTH_TOKEN'))
        self.from_whatsapp = config('TWILIO_WHATSAPP', default=os.getenv('TWILIO_WHATSAPP', config('TWILIO_PHONE', default=os.getenv('TWILIO_PHONE'))))
        
        if not all([self.account_sid, self.auth_token, self.from_whatsapp]):
            raise ValueError("Missing Twilio WhatsApp credentials in .env file")
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_report(self, patient_phone, report_text, pdf_path=None):
        """
        Send medical report via WhatsApp
        
        Args:
            patient_phone: Patient's WhatsApp number (with country code, e.g., +919043890506)
            report_text: Formatted report text
            pdf_path: Path to PDF report file (optional)
        
        Returns:
            str: Message SID on success, None on failure
        """
        try:
            # Ensure phone number is properly formatted
            if not patient_phone.startswith('+'):
                if patient_phone.startswith('91') and len(patient_phone) == 12:
                    patient_phone = '+' + patient_phone
                elif len(patient_phone) == 10:
                    patient_phone = '+91' + patient_phone
            
            # Format WhatsApp numbers
            to_whatsapp = f"whatsapp:{patient_phone}"
            from_whatsapp = f"whatsapp:{self.from_whatsapp}" if not self.from_whatsapp.startswith('whatsapp:') else self.from_whatsapp
            
            # Send message with PDF attachment if provided
            if pdf_path and os.path.exists(pdf_path):
                # First, send the text report
                message = self.client.messages.create(
                    from_=from_whatsapp,
                    to=to_whatsapp,
                    body=report_text
                )
                
                # Then send PDF as media
                with open(pdf_path, 'rb') as f:
                    pdf_message = self.client.messages.create(
                        from_=from_whatsapp,
                        to=to_whatsapp,
                        media_url=f"file://{os.path.abspath(pdf_path)}"
                    )
                
                print(f"✅ WhatsApp messages sent successfully!")
                print(f"   Text Message SID: {message.sid}")
                print(f"   PDF Message SID: {pdf_message.sid}")
                
                return message.sid
            else:
                # Send text only
                message = self.client.messages.create(
                    from_=from_whatsapp,
                    to=to_whatsapp,
                    body=report_text
                )
                
                print(f"✅ WhatsApp message sent successfully!")
                print(f"   Message SID: {message.sid}")
                
                return message.sid
        
        except Exception as e:
            print(f"❌ WhatsApp Error: {str(e)}")
            return None


def send_report_whatsapp(patient_phone, report_text, pdf_path=None):
    """
    Convenience function to send report via WhatsApp
    
    Args:
        patient_phone: Patient's WhatsApp number
        report_text: Formatted report text
        pdf_path: Path to PDF file (optional)
    
    Returns:
        str: Message SID on success, None on failure
    """
    try:
        sender = WhatsAppReportSender()
        return sender.send_report(patient_phone, report_text, pdf_path)
    except Exception as e:
        print(f"❌ Failed to initialize WhatsApp sender: {str(e)}")
        return None
