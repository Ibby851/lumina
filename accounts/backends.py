from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		identifier = kwargs.get('email') or username
		if not identifier or not password:
			return None

		user_model = get_user_model()
		try:
			user = user_model._default_manager.get(email__iexact=identifier)
		except user_model.DoesNotExist:
			try:
				user = user_model._default_manager.get(username__iexact=identifier)
			except user_model.DoesNotExist:
				return None
		except user_model.MultipleObjectsReturned:
			return None

		if user.check_password(password) and self.user_can_authenticate(user):
			return user

		return None
