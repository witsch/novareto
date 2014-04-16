jq(document).ready(function() {
    $('.field-collection-move-up').hide();
    $('.field-collection-move-down').hide();
    $("input[id$=field-artikel]").prop('readonly', true);
    $("input[id$=field-beschreibung]").prop('readonly', true);
});
