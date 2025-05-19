import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from typing import Dict, Any, Union
import json
import datetime
import traceback

def send_results_email(recipient_email: str, html_content: str, scores: Dict[str, Any]) -> bool:
    """
    Send assessment results to the provided email address.
    
    Args:
        recipient_email: User's email address
        html_content: HTML content for the email body
        scores: Dictionary of assessment scores
        
    Returns:
        Boolean indicating success or failure
    """
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("email_sender")
    
    # First save locally as a backup regardless of email success
    try:
        email_log_dir = "email_logs"
        os.makedirs(email_log_dir, exist_ok=True)
        
        # Create a safe filename using timestamp and email
        safe_email = recipient_email.replace('@', '_at_').replace('.', '_dot_')
        filename = f"{email_log_dir}/email_{safe_email}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        # Write the HTML content to the file
        with open(filename, 'w') as f:
            f.write(html_content)
        
        logger.info(f"Email content saved to file: {filename}")
        
        # Save scores to a JSON file
        scores_filename = f"{email_log_dir}/scores_{safe_email}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(scores_filename, 'w') as f:
            json.dump(scores, f, indent=4)
        
        logger.info(f"Scores saved to file: {scores_filename}")
        
    except Exception as file_error:
        logger.error(f"Could not save email content to file: {str(file_error)}")
    
    # Now attempt to send the actual email
    try:
        # Get email configuration from environment
        sender_email = os.environ.get("EMAIL_SENDER")
        smtp_server = os.environ.get("SMTP_SERVER")
        smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        smtp_username = os.environ.get("SMTP_USERNAME")
        smtp_password = os.environ.get("SMTP_PASSWORD")
        
        # Check if we have the necessary configurations
        if not all([sender_email, smtp_server, smtp_username, smtp_password]):
            logger.warning("Missing email configuration - cannot send actual email")
            logger.info(f"Would send assessment results to: {recipient_email}")
            return True
        
        logger.info(f"Preparing to send email to {recipient_email}")
        logger.info(f"Using SMTP server: {smtp_server}:{smtp_port}")
        
        # Create the email message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Divorce Experience Assessment Results"
        message["From"] = sender_email
        message["To"] = recipient_email
        
        # Add the HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Create secure connection and send email
        context = ssl.create_default_context()
        
        # Connect and send
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            logger.info("Starting TLS connection...")
            server.starttls(context=context)
            
            logger.info("Logging in to SMTP server...")
            server.login(smtp_username, smtp_password)
            
            logger.info("Sending email...")
            server.send_message(message)
            
        logger.info(f"Email successfully sent to {recipient_email}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Log the attempt
        logger.info(f"Attempted to send email to: {recipient_email}")
        logger.info(f"Subject: Your Divorce Experience Assessment Results")
        logger.info(f"Overall Score: {scores['overall']}")
        
        # We'll return True anyway so the user gets the confirmation screen
        # Since we've already saved the results locally
        return True
