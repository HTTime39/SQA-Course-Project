class Session:
  user_type = False
  is_active = False
  username = ""

  def __init__(self, user_type, is_active, username):
    self.user_type = user_type
    self.is_active = is_active
    self.username = username