# -*- coding: utf-8 -*-


def find_dict_diff(d1, d2, path=""):
    result = False
    for k in d1.keys():
        if k not in d2:
            continue
        else:
            if type(d1[k]) is dict:
                if path == "":
                    path = k
                else:
                    path = path + "->" + k
                result = self.find_dict_diff(d1[k], d2[k], path)
            else:
                if d1[k] == d2[k]:
                    return True
                elif type(d1[k]) == type(d2[k]) and isinstance(d1[k], list):
                    return len(set(d1[k]).intersection(set(d2[k]))) > 0
    return result


class FilterHostsByHost:
    @staticmethod
    def run(data, conf, **kwargs):
        data_filter = kwargs.get("host_name")
        filtered_targets = list()
        if data_filter in data.targets["hosts"]:
            filtered_targets.append(data_filter)
        data.targets["hosts"] = filtered_targets
        return data


class FilterHostsByTag:
    @staticmethod
    def run(data, conf, **kwargs):
        tag_name = kwargs.get("tag_name")
        tag_value = kwargs.get("tag_value")
        filtered_targets = list()
        for host_name in data.targets["hosts"]:
            host_tags = data.data["hosts"][host_name]
            if tag_name in host_tags and (
                        (isinstance(host_tags[tag_name], str) and host_tags[tag_name] == tag_value) or
                        (isinstance(host_tags[tag_name], list) and any(
                                host_value == tag_value for host_value in host_tags[tag_name]))):
                filtered_targets.append(host_name)
        data.targets["hosts"] = filtered_targets
        return data


class FilterApplicationsByHost:

    @staticmethod
    def run(data, conf, **kwargs):
        host_name = kwargs.get("host_name")
        filtered_data = list()
        if host_name in data.data["hosts"]:
            host_tags = data.data["hosts"][host_name]
            for application_name in data.targets["applications"]:
                application_tags = data.data_target_map["application_hosts"][application_name]
                app_host_tag_match = find_dict_diff(application_tags, host_tags)
                if app_host_tag_match:
                    filtered_data.append(application_name)
        data.targets["applications"] = filtered_data
        return data