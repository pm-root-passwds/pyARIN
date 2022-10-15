#!/usr/bin/python3
import os
import json
import xmltodict
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape
import templates
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PyArin:
    def __init__(self):
        self.url = "https://reg.arin.net/rest"
        self.template_path = templates.__path__[0]
        self.env = Environment(
            loader=FileSystemLoader(self.template_path),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.headers = json.loads(self.env.get_template("headers.json").render())

        self.api_key = os.environ.get("ARIN_API_KEY")

    def by_as_set(self, as_set):
        """

        :param as-set
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """
        get = requests.get(
            f"{self.url}/irr/as-set/{as_set}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)
        # return get.status_code, resp

    def get_ticket_summaries(self, ticket_type=None, ticket_status=None):
        """

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        if not ticket_type or not ticket_status:
            return  # Something useful

        get = requests.get(
            f"{self.url}/ticket/summary;{'ticketType='+ticket_type if ticket_type else ''}{';' if ticket_type and ticket_status else ''}{'ticketStatus='+ticket_status if ticket_status else ''}=ASN_REQUEST?apikey={self.api_key}",
            headers=self.headers,
        )
        print(dir(get))

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)

    def get_roas(self, orghandle):
        """

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        get = requests.get(
            f"{self.url}/roa/{orghandle}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)
        print(doc)
        return get.status_code, json.dumps(doc)

    def submit_roa_req(self, orghandle, resource_class):  # TODO: Test me
        """

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        post = requests.post(
            f"{self.url}/roa/{orghandle};resourceClass={resource_class}??apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(post.text)
        print(doc)
        return post.status_code, json.dumps(doc)

    def submit_roa_req(self, orghandle, resource_class):  # TODO: Test me
        """

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        post = requests.post(
            f"{self.url}/roa/{orghandle};resourceClass={resource_class}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(post.text)
        print(doc)
        return post.status_code, json.dumps(doc)

    def delete_roa(self, roahandle, resource_class):  # TODO: Test me
        """

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        delete = requests.delete(
            f"{self.url}/roa/spec/{roahandle}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(delete.text)
        print(doc)
        return delete.status_code, json.dumps(doc)

    def whowas_asn(self, asn):
        """

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        get = requests.get(
            f"{self.url}/report/whoWas/asn/{asn}?apikey={self.api_key}",
            headers=self.headers,
        )
        print(get.text)
        doc = xmltodict.parse(get.text)
        # print(doc)
        return get.status_code, json.dumps(doc)

    def whowas_ip(self, ip):
        """

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        get = requests.get(
            f"{self.url}/report/whoWas/net/{ip}?apikey={self.api_key}",
            headers=self.headers,
        )
        print(get.text)
        doc = xmltodict.parse(get.text)
        # print(doc)
        return get.status_code, json.dumps(doc)


test = PyArin()
# print(test.get_ticket_summaries(ticket_type="ASN_REQUEST", ticket_status="CLOSED"))
# print(test.get_roas(orghandle='BTL-251'))
print(test.whowas_asn(asn=20055))
