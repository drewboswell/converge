# -*- coding: utf-8 -*-

class FilterApplicationsByHost:
    @staticmethod
    def get_applications_matching_host(applications, host_tags):
        filtered_applications = list()
        for application_name, application_values in applications.items():
            for tag_type, tag_values in host_tags.items():
                if tag_type in application_values:
                    for tag_value in tag_values:
                        if any(x == tag_value for x in application_values[tag_type]):
                            filtered_applications.append(application_name)
        return filtered_applications
