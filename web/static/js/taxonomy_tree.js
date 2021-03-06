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
                    "url": window.apiURLPrefix + "api/taxonomyTree/jsTree",
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
            itemType = data.rslt.obj.attr("type") == "taxonomyCategory" ? "category" : "taxonomy";
            $.ajax({
                type: 'GET',
                url: apiURLPrefix + "api/" + (data.rslt.obj.attr("type") == "taxonomyCategory" ? "category" : "taxonomy") + "/info/" + data.rslt.obj.attr("itemId"),
                dataType: 'json'
            }).done(function (data) {
                    myData = data;
                    var source;

                    if (itemType === "category") {
                        source = $("#category-info-template").html();
                    } else {
                        source = $("#taxonomy-template").html();
                    }

                    var template = Handlebars.compile(source);
                    var html = template(data);

                    $("#taxonomyInfo").html(html);
					$(".handlebars-url").each(function() {
						$(this).attr('href',prepender_url + $(this).attr('href'));
						$(this).attr('href',$(this).attr('href').replace("//","/"));
					});
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

                    $("#oldName").html(data.context.innerText || data.context.textContent);
                    $("#renameForm").attr("action", apiURLPrefix + 'category/rename/' + data.attr("itemid") + '/');
                    $('#renameModal').modal('show');
                } else {
                    window.open(apiURLPrefix + "taxonomy/edit/" + itemId);
                }
            }
        },
        deleteItem: {
            label: "Delete",
            action: function (data) {
                var textContent =  data.context.innerText || data.context.textContent;

                $("#itemToDeleteName").html(textContent.split("(")[0].trim());
                $("#confirmRemove").attr("action", apiURLPrefix + 'taxonomy/delete/' + data.attr("itemid") + '/');
                $('#confirmRemoveModal').modal('show');

            }
        },
        deleteCategory: {
            label: "Delete Category",
            action: function (data) {
                var textContent =  data.context.innerText || data.context.textContent;
                $("#categoryToDeleteName").html(textContent.split("(")[0].trim());
                $("#confirmRemoveCategory").attr("action", apiURLPrefix + 'category/delete/' + data.attr("itemid") + '/');
                $('#confirmRemoveCategoryModal').modal('show');
            }
		},
        splitItem: { // The "split" menu item
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

                var textContent =  data.context.innerText || data.context.textContent;

                $('#originalTaxonomyItem').text(textContent.split("(")[0].trim());
                $("#splitForm").attr("action", apiURLPrefix + 'taxonomy/split/' + data.attr("itemid") + '/');
                $('#splitModal').modal('show');


                $.ajax({
                    type: 'GET',
                    url: apiURLPrefix + "api/taxonomy/info/" + data.attr("itemId"),
                    dataType: 'json'
                }).done(function (data) {

                        var source = $("#reference-list-template").html();
                        var template = Handlebars.compile(source);
                        var html = template(data);

                        $("#originalTaxonomy").html(html);

                    });
            }
        },
        addChild: {
            label: "Add Child",
            action: function (data) {
                var textContent =  data.context.innerText || data.context.textContent;
                $("#parentName").html(textContent.split("(")[0].trim());
                $("#addChildForm").attr("action", apiURLPrefix + 'taxonomy/add_child/' + data.attr("itemid") + '/');
                $('#createChildModal').modal('show');
            }
        },
        addItem: {
            label: "Add Item",
            action: function (data) {
                var textContent =  data.context.innerText || data.context.textContent;
                var itemId = data.attr("itemid");
				$("#createItem_parentName").html(textContent.split("(")[0].trim());
                $("#addItemForm").attr("action", apiURLPrefix + 'taxonomy/add_leaf/' + data.attr("itemid") + '/');
                $('#createItemModal').modal('show');
			}
		},
        moveItem: { // The "moveItem" menu item
            label: "Move Taxonomy",
            action: function (data) {

                $.ajax({
                    type: 'GET',
                    url: apiURLPrefix + "api/taxonomyCategories",
                    dataType: 'json'
                }).done(function (categories) {
                        var sourceId = data.attr("itemid");
                        $('#taxonomyItemToMove').text(sourceId);
                        $("#moveCategoryForm").attr("action", apiURLPrefix + 'taxonomy/move/' + data.attr("itemid") + '/');
                        $('#moveCategoryModal').modal('show');

                        var source = $("#category-list-template").html();
                        var template = Handlebars.compile(source);
                        var html = template(categories);
                        $("#categories").html(html);
                    });
            }
        },
        moveReferences: { // The "moveReferences" menu item
            label: "Move References",
            action: function (data) {
                $.ajax({
                    type: 'GET',
                    url: apiURLPrefix + "api/taxonomyTree/default",
                    dataType: 'json'
                }).done(function (categories) {

                        $("#moveFromTaxonomyReferenceList, #moveToTaxonomyReferenceList").sortable({
                            placeholder: "reference-drop-placeholder",
                            connectWith: ".connectedSortable"
                        }).disableSelection();

                        $("#moveReferenceForm").attr("action", apiURLPrefix + 'taxonomy/move-references/');
                        $('#moveReferencesModal').modal('show');

                        var source = $("#taxonomy-list-template").html();
                        var template = Handlebars.compile(source);
                        var html = template(categories);

                        $("#moveRefFromTaxonomy").html(html);
                        $("#moveRefToTaxonomy").html(html);

                        $("#moveRefFromTaxonomy").val(data.attr("itemId"));
                        countItems();
                        updateReferenceList('#moveRefFromTaxonomy', '#moveFromTaxonomyReferenceList', '#moveFromName');

                    });
            }
        }
    };

    if (node.attr("type") == "taxonomyCategory") {
        delete items.splitItem;
        delete items.deleteItem;
        delete items.moveItem;
        delete items.moveReferences;
        delete items.addChild;
    }
	if(node.attr("type") == "taxonomyItem") {
		delete items.deleteCategory;
		delete items.addItem;
	}

    if (node.attr("type") != "taxonomyCategory" && node.attr("type") != "taxonomyItem") {
        delete items.editItem;
        delete items.splitItem;
        delete items.deleteItem;
        delete items.addChild;
		delete items.addItem;
    }

	//
    // get rid of stuff based on permissions (perms also checked on server side)
	//
	if (!perm_modify_items) {
        delete items.editItem;
        delete items.splitItem;
        delete items.deleteItem;
        delete items.moveItem;
        delete items.moveReferences;
		delete items.addItem;
    }

	if (!perm_modify_categories) {
		delete items.addChild;
		delete items.deleteCategory;
    }

    return items;
}

function searchTree() {
    var value = document.getElementById("search_tree").value;
    $("#taxonomyTree").jstree("close_all", false);
    $("#taxonomyTree").jstree("open", 0);
    $("#taxonomyTree").jstree("search", value);
}
