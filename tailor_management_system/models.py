"""Models for tailor management system."""


class LoginObject(object):
    """Login object have login fields."""

    def __init__(self, username, password):
        """Construct login object."""
        self.username = username
        self.password = password
