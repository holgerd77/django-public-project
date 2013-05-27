
function remove_contenttype_model_selectbox_empty_choices(contenttype_field) {
    type_field_id = "#id_" + contenttype_field + "_type";
    $(type_field_id).find("option").each(function() {
        choices_field_id = "#id_" + contenttype_field + "_id_" + $(this).val();
        $(choices_field_id).children(":first").remove();
    });
}

function change_contenttype_selectbox_choices(contenttype_field) {
    type_field_id = "#id_" + contenttype_field + "_type";
    id_field_id = "#id_" + contenttype_field + "_id";
    choices_field_id = "#id_" + contenttype_field + "_id_" + $(type_field_id).val();

    $(id_field_id).html($(choices_field_id).html());
}
