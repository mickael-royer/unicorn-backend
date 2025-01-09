import logging
import json
from dapr.clients import DaprClient
from .config import DAPR_STATE_STORE

def save_state_to_dapr(key: str, value: dict):
    """Saves state to Dapr."""
    try:
        with DaprClient() as d:
             d.wait(5)
             state_value = json.dumps(value)
             d.save_state(store_name=DAPR_STATE_STORE, key=key, value=state_value)
             logging.info(f"State saved successfully with key: {key}")
    except Exception as e:
       logging.error(f"Error during Dapr State saving {e}")
       raise e


def get_state_from_dapr(key: str) -> dict:
   """Retrieves the state from dapr"""
   try:
      with DaprClient() as d:
         d.wait(5)
         retrieved_state = d.get_state(store_name=DAPR_STATE_STORE, key=key).data
         if retrieved_state:
             return json.loads(retrieved_state)
         else:
              return None
   except Exception as e:
       logging.error(f"Error during Dapr State retrieving {e}")
       raise e