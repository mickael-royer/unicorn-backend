import logging
import pusher

# Configure Pusher
pusher_client = pusher.Pusher(
    app_id='1920401',
    key='404b62fffcad0de861ed',
    secret='32abaa3b99e7f6581b39',
    cluster='eu',
    ssl=True
)

def send_notification(channel: str, event: str, data: dict):
    """
    Sends a notification using Pusher.
    
    Args:
        channel (str): The channel name.
        event (str): The event name.
        data (dict): The data payload to send.
    """
    try:
        pusher_client.trigger(channel, event, data)
        logging.info(f"Notification sent to channel '{channel}' with event '{event}': {data}")
    except Exception as e:
        logging.error(f"Failed to send notification: {e}")
        raise
