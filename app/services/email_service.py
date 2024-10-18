from fastapi import HTTPException
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import SENDGRID_API_KEY, SENDER_EMAIL

def send_email_alert(request):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=request.email,
        subject=f"Weather Alert for {request.city}",
        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4; border-radius: 10px; border: 1px solid #ccc;">
            <h2 style="text-align: center; color: #ff4c4c;">⚠️ Weather Alert for {request.city} ⚠️</h2>
            <p style="font-size: 18px; color: #333;">
                Dear User,
            </p>
            <p style="font-size: 16px; color: #333; line-height: 1.5;">
                We wanted to inform you that the current temperature in <strong>{request.city}</strong> has exceeded the threshold:
            </p>
            <div style="margin: 20px 0; padding: 15px; background-color: #ffeded; border-left: 5px solid #ff4c4c; border-radius: 5px;">
                <p style="font-size: 18px; color: #ff4c4c;">
                    <strong>Temperature: {request.temperature}°C</strong>
                </p>
            </div>
            <p style="font-size: 16px; color: #333;">
                Please take necessary precautions and stay safe. Keep monitoring the weather in your area.
            </p>
            <p style="font-size: 16px; color: #333;">
                Best regards,<br>
                <strong>Weather Monitoring System</strong>
            </p>
        </div>
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))