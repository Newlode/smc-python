"""
User module to hold accounts related to users (admin or local) in the SMC

You can create an Admin User, enable superuser, enable/disable the account,
assign local access to engines, and change the account password for SMC or
engine access.
"""
from smc.base.model import Element, ElementCreator, prepared_request
from smc.api.exceptions import ModificationFailed
from smc.base.util import element_resolver


class UserCommon(object):
    def enable_disable(self):
        """ Toggle enable and disable of administrator account

        :raises: :py:class: `smc.api.exceptions.ModificationFailed`
        :return: None
        """
        self.update(href=self.resource.enable_disable)

    def change_password(self, password):
        """ Change user password

        :param str password: new password
        :return: None
        """
        prepared_request(
            ModificationFailed,
            href=self.resource.change_password,
            params={'password': password}
        ).update()


class AdminUser(UserCommon, Element):
    """ Represents an Adminitrator account on the SMC
    Use the constructor to create the user.

    :param name: name of admin
    :param bool local_admin: should be local admin on specified engines
    :param bool allow_sudo: allow sudo on specified engines
    :param bool superuser: is a super user (no restrictions) in SMC
    :param admin_domain: reference to admin domain, shared by default
    :param list engine_target: ref to engines for local admin access

    Create an Admin::

        admin = AdminUser.create(name='dlepage', superuser=True)

    If modifications are required after you can access the admin and
    make changes::

        admin = AdminUser('dlepage')
        admin.change_password('mynewpassword1')
        admin.enable_disable()
    """
    typeof = 'admin_user'

    def __init__(self, name, **meta):
        super(AdminUser, self).__init__(name, **meta)
        pass

    @classmethod
    def create(cls, name, local_admin=False, allow_sudo=False,
               superuser=False, enabled=True, engine_target=None):
        """
        Create an admin user account.

        :param str name: name of account
        :param bool local_admin: is a local admin only
        :param bool allow_sudo: allow sudo on engines
        :param bool superuser: is a super administrator
        :param bool enabled: is account enabled
        :param str engine_target: engine to allow remote access to
        :raises CreateElementFailed: failure creating element with reason
        :return: href of new element
        :rtype: str
        """
        engines = [] if engine_target is None else engine_target
    
        json = {'name': name,
                'enabled': enabled,
                'allow_sudo': allow_sudo,
                'engine_target': engines,
                'local_admin': local_admin,
                'superuser': superuser}
        
        return ElementCreator(cls, json)

    @property
    def is_enabled(self):
        return self.data.get('enabled')

    def change_engine_password(self, password):
        """ Change Engine password for engines on allowed
        list.

        :param str password: password for engine level
        :raises ModificationFailed: failed setting password on engine
        :return: None
        """
        prepared_request(
            ModificationFailed,
            href=self.resource.change_engine_password,
            params={'password': password}
        ).update()


class ApiClient(UserCommon, Element):
    """
    Represents an API Client
    """
    typeof = 'api_client'

    def __init__(self, name, **meta):
        super(ApiClient, self).__init__(name, **meta)
        pass

    @classmethod
    def create(cls, name, enabled=True, superuser=True):
        """
        Create a new API Client. Once client is created,
        you can create a new password by::

            client = ApiClient('myclient')
            client.change_password('mynewpassword')

        :param str name: name of client
        :param bool enabled: enable client
        :param bool superuser: is superuser account
        :raises CreateElementFailed: failure creating element with reason
        :return: href of new element
        :rtype: str
        """
        json = {'enabled': enabled,
                'name': name,
                'superuser': superuser}

        return ElementCreator(cls, json)

    '''    
    def one_time_password(self, password):
        """
        Generate a one-time password for a single session. As the
        method implies, the password will be expired after single use.
        Use :func:`change_password` if you want a multi-use password.
        
        :param str password: one-time password value
        :raises: :py:class:`smc.api.exceptions.ModificationFailed`
        :return: None
        """
        prepared_request(ModificationFailed,
                         href=self.resource.change_password,
                         params={'one_time_password': password},
                         etag=self.etag,
                         ).update()
    '''
