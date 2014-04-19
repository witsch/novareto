jq(document).ready(function() {
    jq('.field-collection-move-up').hide();
    jq('.field-collection-move-down').hide();
    jq('input[name="form.field.bestellung.add"]').hide();
    jq("input[id$=field-artikel]").prop('readonly', true);
    jq("input[id$=field-artikel]").css('width', '7em');
    jq("input[id$=field-beschreibung]").prop('readonly', true);
    jq("input[id$=field-anzahl]").css('width', '7em');

    jq('fieldset#bghw\\.medienshop\\.lieferung').hide()

    jq("#form-field-lieferung").click(function() {
        jq('fieldset#bghw\\.medienshop\\.lieferung').toggle();
    });
});
