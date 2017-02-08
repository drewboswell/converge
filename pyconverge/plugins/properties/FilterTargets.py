# -*- coding: utf-8 -*-


class FilterHostsByHost:
    @staticmethod
    def run(data, conf, **kwargs):
        data_filter = kwargs.get("host_name")
        filtered_targets = list()
        if data_filter in data.targets["hosts"]:
            filtered_targets.append(data_filter)
        data.targets["hosts"] = filtered_targets
        return data


class FilterApplicationsByHost:

    def find_dict_diff(self, d1, d2, path=""):
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

    def run(self, data, conf, **kwargs):
        host_name = kwargs.get("host_name")
        filtered_data = list()
        if host_name in data.data["hosts"]:
            host_tags = data.data["hosts"][host_name]
            for application_name in data.targets["applications"]:
                application_tags = data.data_target_map["application_hosts"][application_name]
                app_host_tag_match = self.find_dict_diff(application_tags, host_tags)
                if app_host_tag_match:
                    filtered_data.append(application_name)
        data.targets["applications"] = filtered_data
        return data
