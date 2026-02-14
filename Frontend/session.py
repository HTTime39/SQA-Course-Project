class Session:
    """
    Represents a user session within the banking system.
    Stores information about the current user and session state.
    """

    def __init__(self, user_type, username, is_active):
        """
        Constructs a Session object.
        :param user_type: Type of user
        :param username: Username of user (for standard users)
        :param is_active: Boolean indicating whether the session is active
        """
        self.user_type = user_type
        self.username = username
        self.is_active = is_active
