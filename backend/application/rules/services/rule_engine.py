import re
from typing import Optional

from application.commons.services.global_request import get_current_user
from application.core.models import Observation, Product
from application.core.services.observation import (
    get_current_severity,
    get_current_status,
)
from application.core.services.observation_log import create_observation_log
from application.issue_tracker.services.issue_tracker import (
    push_observation_to_issue_tracker,
)
from application.rules.models import Rule


class Rule_Engine:
    def __init__(self, product: Product):
        product_parser_rules = Rule.objects.filter(product=product, enabled=True)
        self.rules: list[Rule] = list(product_parser_rules)

        if product.product_group:
            product_group_parser_rules = Rule.objects.filter(
                product=product.product_group,
                enabled=True,
            )
            self.rules += list(product_group_parser_rules)

        if product.apply_general_rules:
            general_rules = Rule.objects.filter(product__isnull=True, enabled=True)
            self.rules += list(general_rules)

        self.product = product

    def apply_rules_for_observation(self, observation: Observation) -> None:
        previous_product_rule = None
        if observation.product_rule:
            previous_product_rule = observation.product_rule
        previous_general_rule = None
        if observation.general_rule:
            previous_general_rule = observation.general_rule
        observation.product_rule = None
        observation.general_rule = None

        rule_found = False
        for rule in self.rules:
            if (  # pylint: disable=too-many-boolean-expressions
                (not rule.parser or observation.parser == rule.parser)
                and (
                    not rule.scanner_prefix
                    or observation.scanner.lower().startswith(
                        rule.scanner_prefix.lower()
                    )
                )
                and self._check_regex(rule.title, observation.title)
                and self._check_regex(
                    rule.description_observation, observation.description
                )
                and self._check_regex(
                    rule.origin_component_name_version,
                    observation.origin_component_name_version,
                )
                and self._check_regex(
                    rule.origin_docker_image_name_tag,
                    observation.origin_docker_image_name_tag,
                )
                and self._check_regex(
                    rule.origin_endpoint_url, observation.origin_endpoint_url
                )
                and self._check_regex(
                    rule.origin_service_name, observation.origin_service_name
                )
                and self._check_regex(
                    rule.origin_source_file, observation.origin_source_file
                )
                and self._check_regex(
                    rule.origin_cloud_qualified_resource,
                    observation.origin_cloud_qualified_resource,
                )
            ):
                previous_severity = observation.current_severity
                previous_rule_severity = observation.rule_severity
                if rule.new_severity:
                    observation.rule_severity = rule.new_severity
                    observation.current_severity = get_current_severity(observation)

                previous_status = observation.current_status
                previous_rule_status = observation.rule_status
                if rule.new_status:
                    observation.rule_status = rule.new_status
                    observation.current_status = get_current_status(observation)

                if rule.product:
                    observation.product_rule = rule
                else:
                    observation.general_rule = rule

                # Write observation and observation and push to issue tracker log if status or severity has been changed
                if (  # pylint: disable=too-many-boolean-expressions
                    previous_rule_status != observation.rule_status
                    or previous_rule_severity != observation.rule_severity
                    or previous_status != observation.current_status
                    or previous_severity != observation.current_severity
                    or previous_general_rule != observation.general_rule
                    or previous_product_rule != observation.product_rule
                ):
                    self._write_observation_log(
                        observation, rule, previous_severity, previous_status
                    )
                    push_observation_to_issue_tracker(observation, get_current_user())
                rule_found = True
                break

        # Write observation and observation log if no rule was found but there was one before
        if not rule_found and (
            previous_general_rule != observation.general_rule
            or previous_product_rule != observation.product_rule
        ):
            self._write_observation_log_no_rule(
                observation, previous_product_rule, previous_general_rule
            )

    def apply_all_rules_for_product(self) -> None:
        if self.product.is_product_group:
            products = Product.objects.filter(product_group=self.product)
            observations = Observation.objects.filter(product__in=products)
        else:
            observations = Observation.objects.filter(product=self.product)

        for observation in observations:
            self.apply_rules_for_observation(observation)

    def _check_regex(self, pattern: str, value: str) -> bool:
        if not pattern:
            return True

        if not value:
            return False

        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        return compiled_pattern.match(value) is not None

    def _write_observation_log(
        self,
        observation: Observation,
        rule: Rule,
        previous_severity: str,
        previous_status: str,
    ) -> None:
        if previous_status != observation.current_status:
            status = observation.current_status
        else:
            status = ""
        if previous_severity != observation.current_severity:
            severity = observation.current_severity
        else:
            severity = ""

        if rule.product:
            comment = f"Updated by product rule {rule.name}"
        else:
            comment = f"Updated by general rule {rule.name}"

        create_observation_log(observation, severity, status, comment)

    # Write observation and observation log if status or severity has been changed
    def _write_observation_log_no_rule(
        self,
        observation: Observation,
        previous_product_rule: Optional[Rule],
        previous_general_rule: Optional[Rule],
    ) -> None:
        observation.rule_severity = ""
        previous_severity = observation.current_severity
        observation.current_severity = get_current_severity(observation)
        observation.rule_status = ""
        previous_status = observation.current_status
        observation.current_status = get_current_status(observation)

        if previous_status != observation.current_status:
            status = observation.current_status
        else:
            status = ""
        if previous_severity != observation.current_severity:
            severity = observation.current_severity
        else:
            severity = ""

        if previous_product_rule:
            comment = f"Removed product rule {previous_product_rule.name}"
        elif previous_general_rule:
            comment = f"Removed general rule {previous_general_rule.name}"
        else:
            comment = "Removed unkown rule"

        create_observation_log(observation, severity, status, comment)
