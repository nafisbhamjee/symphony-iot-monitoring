"""
Email Notifier - Sends alert emails via Gmail SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EmailNotifier:
    """Handles sending email notifications via Gmail SMTP"""
    
    def __init__(self, smtp_server: str, smtp_port: int, from_email: str,
                 username: str, password: str, to_emails: List[str], enabled: bool = True):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.from_email = from_email
        self.username = username
        self.password = password
        self.to_emails = to_emails
        self.enabled = enabled
        self.emails_sent_success = 0
        self.emails_failed = 0
        
    def send_alert_email(self, rule_name: str, subject: str, body: str,
                        metric_name: str, current_value: float, 
                        threshold: float, condition: str, severity: str) -> bool:
        """Send alert notification email"""
        if not self.enabled:
            logger.info(f"📧 [MOCK MODE] Would send alert email:")
            logger.info(f"   Alert: {rule_name} ({severity})")
            logger.info(f"   Metric: {metric_name} = {current_value} (threshold: {condition} {threshold})")
            logger.info(f"   To: {', '.join(self.to_emails)}")
            logger.info(f"   Subject: {subject}")
            self.emails_sent_success += 1
            return True
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.to_emails)
            msg['Subject'] = subject
            
            html_body, plain_body = self._format_alert_email(
                rule_name, severity, metric_name, 
                current_value, threshold, condition, body
            )
            
            # Attach plain text version first (fallback)
            msg.attach(MIMEText(plain_body, 'plain'))
            # Attach HTML version (preferred)
            msg.attach(MIMEText(html_body, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            self.emails_sent_success += 1
            logger.info(f"✅ Alert email sent successfully")
            return True
            
        except Exception as e:
            self.emails_failed += 1
            logger.error(f"✗ Failed to send email: {e}")
            return False
    
    def send_test_email(self) -> bool:
        """Send a test email to verify configuration"""
        if not self.enabled:
            logger.info("📧 [MOCK MODE] Would send test email to: " + ', '.join(self.to_emails))
            return True
            
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.to_emails)
            msg['Subject'] = "🧪 Test Email - Symphony IoT Alert Engine"
            
            # Plain text version
            plain_text = "This is a test email from Symphony IoT Alert Engine.\n\nIf you received this, your email configuration is working correctly!"
            
            # HTML version
            html_text = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f3f4f6;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <tr>
                        <td style="background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%); padding: 40px; text-align: center; border-radius: 12px 12px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 32px;">🧪</h1>
                            <h2 style="margin: 10px 0 0 0; color: #ffffff; font-size: 24px; font-weight: 600;">Test Email</h2>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 40px; text-align: center;">
                            <div style="display: inline-block; background-color: #DEF7EC; color: #03543F; padding: 12px 24px; border-radius: 20px; margin-bottom: 20px;">
                                <strong>✅ Configuration Successful</strong>
                            </div>
                            <p style="margin: 20px 0; color: #111827; font-size: 16px; line-height: 1.6;">
                                This is a test email from <strong>Symphony IoT Alert Engine</strong>.
                            </p>
                            <p style="margin: 0; color: #6b7280; font-size: 14px; line-height: 1.6;">
                                If you received this message, your email configuration is working correctly! 🎉
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color: #1f2937; padding: 25px; text-align: center; border-radius: 0 0 12px 12px;">
                            <p style="margin: 0; color: #9ca3af; font-size: 12px;">
                                Powered by <strong style="color: #ffffff;">Symphony IoT Alert Engine</strong>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
            
            msg.attach(MIMEText(plain_text, 'plain'))
            msg.attach(MIMEText(html_text, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info("✅ Test email sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to send test email: {e}")
            return False
    
    def _format_alert_email(self, rule_name: str, severity: str, metric_name: str,
                           current_value: float, threshold: float, 
                           condition: str, body: str) -> tuple:
        """Format alert email with professional HTML template and plain text fallback"""
        
        # Determine colors and icons based on severity
        if severity.upper() == 'CRITICAL':
            color = '#DC2626'  # Red
            bg_color = '#FEE2E2'  # Light red
            gradient_start = '#DC2626'
            gradient_end = '#B91C1C'
            icon = '🔥'
            emoji = '🚨'
        elif severity.upper() == 'WARNING':
            color = '#F59E0B'  # Amber
            bg_color = '#FEF3C7'  # Light amber
            gradient_start = '#F59E0B'
            gradient_end = '#D97706'
            icon = '⚠️'
            emoji = '⚡'
        else:
            color = '#3B82F6'  # Blue
            bg_color = '#DBEAFE'  # Light blue
            gradient_start = '#3B82F6'
            gradient_end = '#2563EB'
            icon = 'ℹ️'
            emoji = '📊'
        
        # Get metric-specific emoji
        metric_emoji = '🌡️' if 'temperature' in metric_name.lower() else \
                      '🔋' if 'battery' in metric_name.lower() else \
                      '💧' if 'humidity' in metric_name.lower() else '📊'
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Professional HTML email template
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Alert: {rule_name}</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f3f4f6; line-height: 1.5;">
    <!-- Email Wrapper -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f3f4f6; padding: 40px 20px;">
        <tr>
            <td align="center">
                <!-- Main Container (600px wide for optimal email rendering) -->
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 16px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1); overflow: hidden; max-width: 100%;">
                    
                    <!-- Animated Header with Gradient -->
                    <tr>
                        <td style="background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%); padding: 40px 30px; text-align: center; position: relative;">
                            <div style="font-size: 48px; margin-bottom: 10px;">{icon}</div>
                            <h1 style="margin: 0; color: #ffffff; font-size: 32px; font-weight: 700; letter-spacing: -0.5px;">
                                Alert Triggered
                            </h1>
                            <p style="margin: 12px 0 0 0; color: rgba(255, 255, 255, 0.95); font-size: 15px; font-weight: 500;">
                                Symphony IoT Monitoring System
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Severity Badge -->
                    <tr>
                        <td style="padding: 25px 30px; text-align: center; background-color: #fafafa;">
                            <span style="display: inline-block; background-color: {color}; color: #ffffff; padding: 10px 28px; border-radius: 24px; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1.2px; box-shadow: 0 4px 12px {color}44;">
                                {emoji} {severity.upper()}
                            </span>
                        </td>
                    </tr>
                    
                    <!-- Main Content Area -->
                    <tr>
                        <td style="padding: 30px 30px 20px 30px;">
                            
                            <!-- Alert Name Card -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: linear-gradient(to right, {bg_color} 0%, #ffffff 100%); border-radius: 12px; border-left: 5px solid {color}; margin-bottom: 25px; overflow: hidden;">
                                <tr>
                                    <td style="padding: 20px 25px;">
                                        <p style="margin: 0; color: #6b7280; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Alert Name</p>
                                        <p style="margin: 8px 0 0 0; color: #111827; font-size: 22px; font-weight: 700;">{rule_name.replace('_', ' ').title()}</p>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Metric Details Box -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f9fafb; border-radius: 12px; margin-bottom: 25px; border: 1px solid #e5e7eb;">
                                <tr>
                                    <td style="padding: 25px;">
                                        <!-- Metric Name -->
                                        <div style="margin-bottom: 20px;">
                                            <p style="margin: 0; color: #6b7280; font-size: 12px; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600;">Metric</p>
                                            <p style="margin: 8px 0 0 0; color: #111827; font-size: 16px; font-weight: 600; font-family: 'Courier New', Monaco, monospace; background-color: #ffffff; padding: 8px 12px; border-radius: 6px; display: inline-block;">
                                                {metric_emoji} {metric_name}
                                            </p>
                                        </div>
                                        
                                        <!-- Current Value vs Threshold -->
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <!-- Current Value (Left) -->
                                                <td width="50%" style="padding: 15px; background-color: #ffffff; border-radius: 8px; vertical-align: top;">
                                                    <p style="margin: 0; color: #6b7280; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Current Value</p>
                                                    <p style="margin: 10px 0 0 0; color: {color}; font-size: 36px; font-weight: 800; line-height: 1;">
                                                        {current_value}
                                                    </p>
                                                </td>
                                                
                                                <!-- Spacer -->
                                                <td width="20" style="padding: 0;"></td>
                                                
                                                <!-- Threshold (Right) -->
                                                <td width="50%" style="padding: 15px; background-color: #ffffff; border-radius: 8px; vertical-align: top;">
                                                    <p style="margin: 0; color: #6b7280; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Threshold</p>
                                                    <p style="margin: 10px 0 0 0; color: #111827; font-size: 32px; font-weight: 700; line-height: 1;">
                                                        {condition} {threshold}
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Alert Message Box -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: {bg_color}; border-radius: 12px; border-left: 5px solid {color}; margin-bottom: 25px;">
                                <tr>
                                    <td style="padding: 25px;">
                                        <p style="margin: 0; color: #111827; font-size: 15px; line-height: 1.7; font-weight: 500;">
                                            {body.replace(chr(10), '<br>')}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Timestamp -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td style="text-align: center; padding: 20px 0;">
                                        <p style="margin: 0; color: #6b7280; font-size: 13px;">
                                            <span style="display: inline-block; background-color: #f3f4f6; padding: 8px 16px; border-radius: 20px;">
                                                🕐 {timestamp}
                                            </span>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                        </td>
                    </tr>
                    
                    <!-- Info Notice -->
                    <tr>
                        <td style="padding: 0 30px 30px 30px;">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-radius: 10px; padding: 18px 22px; border: 1px solid #bfdbfe;">
                                <tr>
                                    <td>
                                        <p style="margin: 0; color: #1e40af; font-size: 13px; line-height: 1.6; font-weight: 500;">
                                            <strong>ℹ️ Note:</strong> This alert will not repeat for <strong>15 minutes</strong> to prevent notification spam. You will be notified again if the condition persists after the cooldown period.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%); padding: 30px; text-align: center; border-radius: 0 0 16px 16px;">
                            <p style="margin: 0; color: #ffffff; font-size: 14px; font-weight: 600; letter-spacing: 0.5px;">
                                ⚙️ Symphony IoT Alert Engine
                            </p>
                            <p style="margin: 10px 0 0 0; color: #9ca3af; font-size: 12px; line-height: 1.5;">
                                Orchestrated monitoring for intelligent IoT systems<br>
                                Powered by Eclipse Symphony
                            </p>
                        </td>
                    </tr>
                    
                </table>
                
                <!-- Footer Disclaimer (Outside main box) -->
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="margin-top: 20px; max-width: 100%;">
                    <tr>
                        <td style="text-align: center; padding: 0 20px;">
                            <p style="margin: 0; color: #6b7280; font-size: 11px; line-height: 1.5;">
                                This is an automated alert from your IoT monitoring system.<br>
                                For support, please check your system logs or contact your administrator.
                            </p>
                        </td>
                    </tr>
                </table>
                
            </td>
        </tr>
    </table>
</body>
</html>"""
        
        # Plain text fallback for email clients that don't support HTML
        plain_text = f"""
{'='*60}
{icon} ALERT TRIGGERED - {severity.upper()}
{'='*60}

Alert Name: {rule_name}
Severity: {severity.upper()}

{'─'*60}
METRIC DETAILS
{'─'*60}
Metric:         {metric_name}
Current Value:  {current_value}
Threshold:      {condition} {threshold}

{'─'*60}
DESCRIPTION
{'─'*60}
{body}

{'─'*60}
Timestamp: {timestamp}
{'─'*60}

Note: This alert will not repeat for 15 minutes to prevent spam.

{'='*60}
Powered by Symphony IoT Alert Engine
Orchestrated monitoring for intelligent IoT systems
{'='*60}
"""
        
        return html, plain_text
    
    def get_stats(self) -> dict:
        """Get email statistics"""
        total = self.emails_sent_success + self.emails_failed
        return {
            'emails_sent': self.emails_sent_success,
            'emails_failed': self.emails_failed,
            'success_rate': (self.emails_sent_success / total * 100) if total > 0 else 0
        }
