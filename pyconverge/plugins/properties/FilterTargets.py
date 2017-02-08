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

