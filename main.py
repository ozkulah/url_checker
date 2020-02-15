import os

import dns.resolver
import pandas as pd

import socket

class UrlExtractor:

    def __init__(self):
        self.categories = None
        self.dataset = None
        self.category_label = "main_category"
        self.category_accuracy_label = "main_category:confidence"
        self.domain_label = "url"

    def read_csv_by_categories(self, csv_file):
        dataset = pd.read_csv(filepath_or_buffer=csv_file, usecols=[self.category_label, self.category_accuracy_label, self.domain_label])
        high_confidence = dataset[self.category_accuracy_label] > 0.8
        actual_ones = dataset[self.category_label] != "Not_working"
        dataset_update = dataset[high_confidence]
        dataset_update = dataset_update[actual_ones]
        self.categories = list(dataset_update[self.category_label])
        self.dataset = dataset_update


    def is_actual_ip(self, ip_addr):
        """
            This method checks ip address
        """
        try:
            socket.inet_aton(ip_addr)
            return True
        except socket.error:
            return False

    def is_active_domain(self, domain="www.google.com", name_server='1.1.1.1'):
            """
            This method send a dns request and if there is an ip
            that means domain is an active domain
            """
            my_resolver = dns.resolver.Resolver()
            my_resolver.nameservers = [name_server]
            my_resolver.timeout = 3
            my_resolver.lifetime = 3
            try:
                A = my_resolver.query(domain, 'A')
                for i in A.response.answer:
                    for j in i.items:
                        return self.is_actual_ip(str(j))
            except Exception as e:
                return None

    def filter_active_domains(self, csv_file):
        """
        This method filter and find active domains for each category
        and write that info into the files
        """
        self.read_csv_by_categories(csv_file)
        for index, row in self.dataset.iterrows():
            if self.is_active_domain(row[self.domain_label]):
                self.write_domains_to_file_by_category(row[self.category_label], row)

    def write_domains_to_file_by_category(self, file_name, row):
        """
        This method write domain name and category into file
        """
        with open("output/"+file_name+".csv", "a+") as f:
            f.write(row[self.domain_label] + "," + row[self.category_label] + "\n")


if __name__ == '__main__':
    urlext = UrlExtractor()
    urlext.filter_active_domains("URL-categorization-DFE.csv")
