class Session:
  is_admin = False
  is_active = False
  username = ""

  def __init__(self, is_admin, is_active, username):
    self.is_admin = is_admin
    self.is_active = is_active
    self.username = username