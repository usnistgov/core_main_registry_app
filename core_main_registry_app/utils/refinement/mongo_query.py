"""
Mongo query creation for the refinements.
"""

import logging

from core_main_app.commons import exceptions as exceptions
from core_main_registry_app.components.category import api as category_api

logger = logging.getLogger("core_main_registry_app.utils.refinement.mongo_query")


def build_refinements_query(refinements):
    """ Build the refinements query.

    Args:
        refinements:

    Returns:

    """
    or_queries = []
    and_query = {}

    try:
        # transform the refinement in mongo query
        for refinement in refinements:
            queries = dict()
            in_queries = {}
            # For each category in the refinement
            for category_id in refinement:
                try:
                    # Get category
                    category = category_api.get_by_id(category_id)
                    dot_notation = category.path
                    value = category.value
                    # If dot notation already exists, append to the dict
                    if dot_notation in queries:
                        queries[dot_notation].append(value)
                    # Create a dict with the dot notation as the key
                    else:
                        queries[dot_notation] = [value]
                except (exceptions.DoesNotExist, Exception), e:
                    logger.warning("Impossible to find the category ({0}): {1}."
                                   .format(str(len(category_id)), e.message))

            for query in queries:
                # Create the query with $in
                key = query
                values = ({'$in': queries[query]})
                in_queries[key] = values
                # Case of the element has attributes
                in_queries[key + ".#text"] = values

            if len(in_queries) > 0:
                # $or between categories belonging to the same refinement
                or_queries.append({'$or': [{x: in_queries[x]} for x in in_queries]})

        if len(or_queries) > 0:
            # $and between refinements
            and_query = {'$and': or_queries}

        return and_query
    except Exception, e:
        logger.error("Something went wrong during the creation of the refinement query. Search "
                     "won't be refined: {0}.".format(e.message))
        return {}
