$(function () {
    $("#taxonomyTree")
        .bind("before.jstree", function (e, data) {
            $("#alog").append(data.func + "<br />");
        })
        .jstree({
            // List of active plugins
            "plugins": [
                "themes", "json_data", "ui", "crrm", "search", "types", "hotkeys", "contextmenu"
            ],

            "themes": {
                "theme": "default",
                "dots": true,
                "icons": false
            },

            "contextmenu": {items: customMenu},


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
                url: "/api/taxonomy/info/" + data.rslt.obj.attr("itemId"),
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


});

function customMenu(node) {
    // The default set of all items
    var items = {
        editItem: { // The "rename" menu item
            label: "Edit",
            action: function (data) {

                var itemId = data.attr("itemid");
                var itemType = data.attr("type");

                if (itemType == "taxonomyCategory") {
                    $("#oldName").html(data.context.innerText);
                    $("#renameForm").attr("action", '/category/rename/' + data.attr("itemid") + '/');
                    $('#renameModal').modal('show');
                } else {
                    window.open("/taxonomy/edit/" + itemId);
                }
            }
        },
        deleteItem: { // The "rename" menu item
            label: "Delete",
            action: function (data) {
                $("#itemToDeleteName").html(data.context.innerText.split("(")[0].trim());
                $("#confirmRemove").attr("action", '/taxonomy/delete/' + data.attr("itemid") + '/');
                $('#confirmRemoveModal').modal('show');

            }
        },

        splitItem: { // The "delete" menu item
            label: "Split",
            action: function (data) {
                $("#originalTaxonomy, #newTaxonomy").sortable({
                    placeholder: "reference-drop-placeholder",
                    connectWith: ".connectedSortable"
                }).disableSelection();

                // reset form fields in the event that they were populated before :)
                $("#split_detail_group").toggleClass("control-group error", false);
                $("#split_errors").html('');
                $("#originalTaxonomyItemCount").text('');
                $("#newTaxonomyItemCount").text('');
                $("#newTaxonomy").html('');

                $('#originalTaxonomyItem').text(data.context.innerText.split("(")[0].trim());
                $("#splitForm").attr("action", '/taxonomy/split/' + data.attr("itemid") + '/');
                $('#splitModal').modal('show');

                $.ajax({
                    type: 'GET',
                    url: "/api/taxonomy/info/" + data.attr("itemId"),
                    dataType: 'json'
                }).done(function (data) {
                        myData = data;
                        console.log(myData);
                        var source = $("#reference-list-template").html();
                        var template = Handlebars.compile(source);
                        var html = template(data);

                        $("#originalTaxonomy").html(html);

                    });
            }
        },
        moveItem: { // The "delete" menu item
            label: "Move",
            action: function (data) {
                console.log("I've got to move it, move it.")
            }
        }
    };

    if (node.attr("type") == "taxonomyCategory") {
        delete items.splitItem;
        delete items.deleteItem;
        delete items.moveItem;
    }

    if (node.attr("type") != "taxonomyCategory" && node.attr("type") != "taxonomyItem") {
        delete items.editItem;
        delete items.splitItem;
        delete items.deleteItem;
    }

    return items;
}

function searchTree() {

    var value = document.getElementById("search_tree").value;
    $("#taxonomyTree").jstree("close_all", false);
    $("#taxonomyTree").jstree("open", 0);
    $("#taxonomyTree").jstree("search", value);


}