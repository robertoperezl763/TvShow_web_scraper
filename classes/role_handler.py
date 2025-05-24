class RoleHandler:
  role_to_attribute = {
      'Director': 'director',
      'Executive Producer': 'executive_producer',
      'Screenwriter': 'screenwriter'
  }

  def add_role_data(self, role, value):

    classAttribute = RoleHandler.role_to_attribute.get(role)

    if classAttribute:
      setattr(self, classAttribute, value)
    else:
      print(f'--Role given: {role} not found. Skipping this.')



