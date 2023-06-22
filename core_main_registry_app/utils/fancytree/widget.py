"""
FancyTree widget.
Based on xrmx work: https://github.com/xrmx/django-fancytree.
Modified for the registry project.
"""
from itertools import chain

from django import forms
from django.conf import settings
from django.forms.widgets import Widget
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_str
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from mptt.templatetags.mptt_tags import cache_tree_children

FANCYTREE_CDN_PATH = (
    "https://cdnjs.cloudflare.com/ajax/libs/jquery.fancytree/2.38.3"
)

try:
    import simplejson as json
except ImportError:
    import json


def get_doc(node, values, count_mode):
    """Represent a node.

    Args:
        node:
        values:
        count_mode:  Add an html element to display counts next to each node (True/False).

    Returns:

    """
    if hasattr(node, "get_doc"):
        return node.get_doc(values)
    if hasattr(node, "name"):
        name = node.name
    else:
        name = str(node)

    #  Add an html element to display counts next to each node.
    if count_mode:
        count_html = "<em class='occurrences' id='{0}'></em>".format(node.pk)
        doc = {"title": "{0} {1}".format(name, count_html), "key": node.pk}
    else:
        doc = {"title": name, "key": node.pk}

    if str(node.pk) in values:
        doc["selected"] = True
        doc["expand"] = True
    return doc


def recursive_node_to_dict(node, values, count_mode):
    """recursive node to dict.

    Args:
        node:
        values:
        count_mode:

    Returns:

    """
    result = get_doc(node, values, count_mode)
    children = [
        recursive_node_to_dict(c, values, count_mode)
        for c in node.get_children()
    ]
    if children:
        expand = [c for c in children if c.get("selected", False)]
        if expand:
            result["expand"] = True
        result["folder"] = True
        result["children"] = children
    return result


def get_tree(nodes, values, count_mode):
    """get tree.

    Args:
        nodes:
        values:
        count_mode:

    Returns:

    """
    root_nodes = cache_tree_children(nodes)
    return [recursive_node_to_dict(n, values, count_mode) for n in root_nodes]


class FancyTreeWidget(Widget):
    """Fancy Tree Widget"""

    def __init__(
        self,
        attrs=None,
        choices=(),
        queryset=None,
        select_mode=3,
        count_mode=False,
    ):
        """

        Args:
            attrs:
            choices:
            queryset:
            select_mode:
            count_mode: Add an html element to display counts next to each node (True/False).

        """
        super().__init__(attrs)
        self.queryset = queryset
        self.select_mode = select_mode
        self.choices = list(choices)
        self.count_mode = count_mode

    def value_from_datadict(self, data, files, name):
        """value from datadict

        Args:
            data:
            files:
            name:

        Returns:

        """

        if isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name, None)

    def render(self, name, value, attrs=None, choices=(), renderer=None):
        """render

        Args:
            name:
            value:
            attrs:
            choices:
            renderer:

        Returns:

        """
        if value is None:
            value = []
        if not isinstance(value, (list, tuple)):
            value = [value]
        has_id = attrs and "id" in attrs
        final_attrs = self.build_attrs(attrs)
        if has_id:
            output = [
                '<div id="%s" name="%s"></div>'
                % (attrs["id"], self.choices.field.label)
            ]
            id_attr = ' id="%s_checkboxes"' % (attrs["id"])
        else:
            output = ['<div name="%s"></div>' % self.choices.field.label]
            id_attr = ""
        output.append(
            '<ul style="display: none;" class="fancytree_checkboxes"%s>'
            % id_attr
        )
        str_values = set([force_str(v) for v in value])
        for i, (option_value, option_label) in enumerate(
            chain(self.choices, choices)
        ):
            if has_id:
                final_attrs = dict(
                    final_attrs, id="%s_%s" % (attrs["id"], option_value)
                )
                label_for = ' for="%s"' % final_attrs["id"]
            else:
                label_for = ""

            checkbox = forms.CheckboxInput(
                final_attrs, check_test=lambda value: value in str_values
            )
            option_value = force_str(option_value)
            rendered_cb = checkbox.render(name, option_value)
            option_label = conditional_escape(force_str(option_label))
            output.append(
                "<li><label%s>%s %s</label></li>"
                % (label_for, rendered_cb, option_label)
            )
        output.append("</ul>")
        output.append('<script type="text/javascript">')
        js_data_var = "fancytree_data_%s" % (attrs["id"].replace("-", "_"))
        if has_id:
            output.append(
                "var %s = %s;"
                % (
                    js_data_var,
                    json.dumps(
                        get_tree(self.queryset, str_values, self.count_mode)
                    ),
                )
            )
            output.append(
                """
                var defer_initFancyTree = function() {
                    $.when(
                        cachedScript( "%(fancytree)s" ),
                        $.Deferred(function( deferred ){
                            $( deferred.resolve );
                        })
                    ).done(function(){
                        $.when(
                            $.Deferred(function( deferred ){
                                $( deferred.resolve );
                            })
                        ).done(function(){
                            $("#%(id)s").fancytree({
                                extensions: ["glyph"],
                                checkbox: true,
                                icon: false,
                                selectMode: %(select_mode)d,
                                source: %(js_var)s,
                                debugLevel: %(debug)d,
                                glyph: {
                                    map: {
                                        expanderClosed: "fa-solid fa-caret-right",
                                        expanderLazy: "fa-solid fa-caret-right",
                                        expanderOpen: "fa-solid fa-caret-down",
                                        checkbox: "fa-regular fa-square",
                                        checkboxSelected: "fa-regular fa-square-check",
                                        checkboxUnknown: "fa-regular fa-square-minus",
                                    }
                                },
                                customTag : {
                                    tag: "div"
                                },
                                _classNames: {
                                    active: "no-css",
                                    focused: "no-css"
                                },
                                select: function(event, data) {
                                    $('#%(id)s_checkboxes').find('input[type=checkbox]').prop('checked', false);
                                    var selNodes = data.tree.getSelectedNodes();
                                    var selKeys = $.map(selNodes, function(node){
                                           $('#%(id)s_' + (node.key)).prop('checked', true);
                                           return node.key;
                                    });
                                    // trigger the event fancy_tree_select
                                    $(document).trigger("fancy_tree_select_event", data);
                                },
                                click: function(event, data) {
                                    var node = data.node;
                                    if (event.targetType == "fancytreeclick")
                                        node.toggleSelected();
                                },
                                keydown: function(event, data) {
                                    var node = data.node;
                                    if (event.which == 32) {
                                        node.toggleSelected();
                                        return false;
                                    }
                                },
                                init: function(event, data) {
                                    // Render all nodes even if collapsed
                                    data.tree.getRootNode().render(force=true, deep=true);
                                    // set a timeout to let the tree finish its rendering
                                    setTimeout(function(){
                                        // trigger the event fancy_tree_ready
                                        $(document).trigger("fancy_tree_ready_event", data);
                                    }, 200);
                                },
                            });
                        });
                    });
                };
                onjQueryReady(defer_initFancyTree);

                """
                % {
                    "id": attrs["id"],
                    "js_var": js_data_var,
                    "debug": settings.DEBUG and 1 or 0,
                    "select_mode": self.select_mode,
                    "fancytree": f"{FANCYTREE_CDN_PATH}/jquery.fancytree-all-deps.min.js",
                }
            )
        output.append("</script>")
        return mark_safe("\n".join(output))

    class Media:
        """Media"""

        js = ("core_explore_common_app/common/js/tools.js",)

        css = {
            "all": (
                f"{FANCYTREE_CDN_PATH}/skin-bootstrap/ui.fancytree.min.css",
                "core_main_registry_app/user/css/fancytree/fancytree.custom.css",
            )
        }
