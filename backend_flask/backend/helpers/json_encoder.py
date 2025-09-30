import uuid
from json import JSONEncoder

class UUIDJSONEncoder(JSONEncoder):
    """Custom JSON encoder that converts UUID objects to strings."""

    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)

        return super().default(obj)