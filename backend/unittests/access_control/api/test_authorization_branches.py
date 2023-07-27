from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationBranches(TestAuthorizationBase):
    def test_authorization_branches(self):
        expected_data = "OrderedDict([('count', 3), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('is_default_branch', True), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('name', 'db_branch_internal_dev'), ('product', 1)]), OrderedDict([('id', 2), ('is_default_branch', False), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('name', 'db_branch_internal_main'), ('product', 1)]), OrderedDict([('id', 3), ('is_default_branch', True), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('name', 'db_branch_external'), ('product', 2)])])])"
        self._test_api(
            APITest("db_admin", "get", "/api/branches/", None, 200, expected_data)
        )

        expected_data = "OrderedDict([('count', 2), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('is_default_branch', True), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('name', 'db_branch_internal_dev'), ('product', 1)]), OrderedDict([('id', 2), ('is_default_branch', False), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('name', 'db_branch_internal_main'), ('product', 1)])])])"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'id': 1, 'is_default_branch': True, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_branch_internal_dev', 'product': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/1/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'No Branch matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/3/",
                None,
                404,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/99999/",
                None,
                404,
                expected_data,
            )
        )

        post_data = {"name": "string", "product": 1}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/branches/",
                post_data,
                403,
                expected_data,
            )
        )

        expected_data = "{'id': 4, 'is_default_branch': False, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'string', 'product': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/branches/",
                post_data,
                201,
                expected_data,
            )
        )

        post_data = {"name": "changed"}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/branches/1/",
                post_data,
                403,
                expected_data,
            )
        )

        expected_data = "{'id': 1, 'is_default_branch': True, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'changed', 'product': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/branches/1/",
                post_data,
                200,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "delete",
                "/api/branches/1/",
                None,
                403,
                expected_data,
            )
        )

        expected_data = "{'message': \"Cannot delete some instances of model 'Branch' because they are referenced through protected foreign keys\"}"
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/branches/1/",
                None,
                409,
                expected_data,
            )
        )