from .base_api import BaseAPI


class AutomationApi(BaseAPI):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.base_url = base_url

    def get_product_list(self) -> object:
        """
        Get products list

        :return: response object
        """
        resp = self._get(path="/productsList")
        return resp

    def get_brand_list(self) -> object:
        """
        Get brand list

        :return: response object
        """
        resp = self._get(path=f"/brandsList")
        return resp

    def search_product(self, data: str) -> object:
        """
        Search  for a product

        :data: product for search

        :return: response object
        """
        search_data = {
            "search_product": data
        }
        resp = self._post(path=f"searchProduct", data=search_data, json={})
        return resp

    def verify_login(self, email: str, password: str) -> object:
        """
        Verify provided login

        :email: email of user
        :password: user password
        :return: response object
        """
        data = {
            "email": email,
            "password": password
        }
        resp = self._post(path=f"/verifyLogin", data=data, json={})
        return resp

    def create_user(self, user_data: dict) -> object:
        """
        Create new user

        :data: user information
            :name
            :email,
            :password,
            :title (for example: Mr, Mrs, Miss),
            :birth_date,
            :birth_month,
            :birth_year,
            :firstname,
            :lastname,
            :company,
            :address1,
            :address2,
            :country,
            :zipcode,
            :state,
            :city,
            :mobile_number

        :return: response object
        """
        data = {
            "name": user_data["name"],
            "email": user_data["email"],
            "password": user_data["password"],
            "title": user_data["title"],
            "birth_date": user_data["birth_date"],
            "birth_month": user_data["birth_month"],
            "birth_year": user_data["birth_year"],
            "firstname": user_data["firstname"],
            "lastname": user_data["lastname"],
            "company": user_data["company"],
            "address1": user_data["address1"],
            "address2": user_data["address2"],
            "country": user_data["country"],
            "zipcode": user_data["zipcode"],
            "state": user_data["state"],
            "city": user_data["city"],
            "mobile_number": user_data["mobile_number"],
        }
        resp = self._post(path=f"createAccount", data=data, json={})
        return resp

    def delete_user(self, email: str, password: str) -> object:
        """
        Delete provided user

        :email: email of user
        :password: user password

        :return: response object
        """
        data = {
            "email": email,
            "password": password
        }
        resp = self._delete(path=f"/deleteAccount", data=data, json={})
        return resp

    def update_user(self, user_data: dict) -> object:
        """
        Update user information

        :data: user information
            :name
            :email,
            :password,
            :title (for example: Mr, Mrs, Miss),
            :birth_date,
            :birth_month,
            :birth_year,
            :firstname,
            :lastname,
            :company,
            :address1,
            :address2,
            :country,
            :zipcode,
            :state,
            :city,
            :mobile_number

        :return: response object
        """
        data = {
            "name": user_data["name"],
            "email": user_data["email"],
            "password": user_data["password"],
            "title": user_data["title"],
            "birth_date": user_data["birth_date"],
            "birth_month": user_data["birth_month"],
            "birth_year": user_data["birth_year"],
            "firstname": user_data["firstname"],
            "lastname": user_data["lastname"],
            "company": user_data["company"],
            "address1": user_data["address1"],
            "address2": user_data["address2"],
            "country": user_data["country"],
            "zipcode": user_data["zipcode"],
            "state": user_data["state"],
            "city": user_data["city"],
            "mobile_number": user_data["mobile_number"],
        }
        resp = self._put(path=f"updateAccount", data=data, json={})
        return resp
