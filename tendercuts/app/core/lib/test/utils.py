import app.core.lib.magento as mage

class GetUser:
    """Return in request User id."""
    def __init__(self):
        """initialize request user id.

        Returns:
            Get the user id from the request
            username contains u:18963 => 18963 is the magento IDS

        """
        self.user = self.request.user
        self.user_id = self.user.username.split(":")

        if len(self.user_id) < 1:
            self.user_id = None
        else:
            self.user_id = self.user_id[1]

        return self.user_id