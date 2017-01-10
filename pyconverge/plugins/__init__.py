# Todo: Validators
# Todo: Readers
# Todo: PreFilters
# Todo: Resolvers
# # Todo: Hierarchies
# Todo: PostFilters
# # Todo: Placeholders


"""
validators: returns key: boolean (dict)
readers: takes previous data and returns all data (dict)
pre-filters: takes all data, and returns all data (dict)
resolvers: uses hierarchy to resolve data, returns all resolved data (dict)
post-filters: takes all resolved data and returns all filtered data
writers: takes all take and outputs it according to given class(es)

##
filters could be considered one unified type?
## all other than validators, should take and return a dict() containing all data
"""