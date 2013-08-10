$(function () {
    $("#taxonomyTree")
        .bind("before.jstree", function (e, data) {
            $("#alog").append(data.func + "<br />");
        })
        .jstree({
            // List of active plugins
            "plugins": [
                "themes", "json_data", "ui", "crrm", "dnd", "search", "types", "hotkeys", "contextmenu"
            ],

            "themes": {
                "theme": "default",
                "dots": true,
                "icons": false
            },


            // I usually configure the plugin that handles the data first
            // This example uses JSON as it is most common
            "json_data": {
                // This tree is ajax enabled - as this is most common, and maybe a bit more complex
                // All the options are almost the same as jQuery's AJAX (read the docs)
                "ajax": {
                    // the URL to fetch the data
                    "url": "/api/taxonomyTree/",
                    // the `data` function is executed in the instance's scope
                    // the parameter is the node being loaded
                    // (may be -1, 0, or undefined when loading the root nodes)
                    "data": function (n) {
                        // the result is fed to the AJAX request `data` option
                        return {
                            "operation": "get_children",
                            "id": n.attr ? n.attr("id").replace("node_", "") : 1
                        };
                    }
                }
            }
        })
        .bind("select_node.jstree", function (event, data) {
            // `data.rslt.obj` is the jquery extended node that was clicked
            // TODO: Load and display taxonomy category and taxonomy items.


            $.ajax({
                type: 'GET',
                url: "/api/taxonomy/" + data.rslt.obj.attr("itemId"),
                dataType: 'json'
            }).done(function (data) {
                    myData = data;
                    console.log(myData);
                    var source = $("#taxonomy-template").html();
                    var template = Handlebars.compile(source);
                    var html = template(data);

                    $("#taxonomyInfo").html(html);

                });

        })

        .bind("create.jstree", function (e, data) {
            $.post(
                "/static/v.1.0pre/_demo/server.php",
                {
                    "operation": "create_node",
                    "id": data.rslt.parent.attr("id").replace("node_", ""),
                    "position": data.rslt.position,
                    "title": data.rslt.name,
                    "type": data.rslt.obj.attr("rel")
                },
                function (r) {
                    if (r.status) {
                        $(data.rslt.obj).attr("id", "node_" + r.id);
                    }
                    else {
                        $.jstree.rollback(data.rlbk);
                    }
                }
            );
        })
        .bind("remove.jstree", function (e, data) {
            data.rslt.obj.each(function () {
                $.ajax({
                    async: false,
                    type: 'POST',
                    url: "/static/v.1.0pre/_demo/server.php",
                    data: {
                        "operation": "remove_node",
                        "id": this.id.replace("node_", "")
                    },
                    success: function (r) {
                        if (!r.status) {
                            data.inst.refresh();
                        }
                    }
                });
            });
        })
        .bind("rename.jstree", function (e, data) {
            $.post(
                "/static/v.1.0pre/_demo/server.php",
                {
                    "operation": "rename_node",
                    "id": data.rslt.obj.attr("id").replace("node_", ""),
                    "title": data.rslt.new_name
                },
                function (r) {
                    if (!r.status) {
                        $.jstree.rollback(data.rlbk);
                    }
                }
            );
        })
        .bind("move_node.jstree", function (e, data) {
            data.rslt.o.each(function (i) {
                $.ajax({
                    async: false,
                    type: 'POST',
                    url: "/static/v.1.0pre/_demo/server.php",
                    data: {
                        "operation": "move_node",
                        "id": $(this).attr("id").replace("node_", ""),
                        "ref": data.rslt.cr === -1 ? 1 : data.rslt.np.attr("id").replace("node_", ""),
                        "position": data.rslt.cp + i,
                        "title": data.rslt.name,
                        "copy": data.rslt.cy ? 1 : 0
                    },
                    success: function (r) {
                        if (!r.status) {
                            $.jstree.rollback(data.rlbk);
                        }
                        else {
                            $(data.rslt.oc).attr("id", "node_" + r.id);
                            if (data.rslt.cy && $(data.rslt.oc).children("UL").length) {
                                data.inst.refresh(data.inst._get_parent(data.rslt.oc));
                            }
                        }
                        $("#analyze").click();
                    }
                });
            });
        });

});

function searchTree() {

    var value = document.getElementById("search_tree").value;
    $("#taxonomyTree").jstree("close_all", false);
    $("#taxonomyTree").jstree("open", 0);
    $("#taxonomyTree").jstree("search", value);


}