$(document).ready(function() {
    $('.field-collection-move-up').hide();
    $('.field-collection-move-down').hide();
    $('input[name="form.field.bestellung.add"]').hide();
    $("input[id$=field-artikel]").prop('readonly', true);
    $("input[id$=field-artikel]").css('width', '4em');
    $("input[id$=field-bestellnummer]").prop('readonly', true);
    $("input[id$=field-bestellnummer]").css('width', '7em');
    $("input[id$=field-beschreibung]").prop('readonly', true);
    $("input[id$=field-anzahl]").css('width', '2em');

    $('fieldset#bghw\\.medienshop\\.lieferung').hide()

    $("#form-field-lieferung").click(function() {
        $('fieldset#bghw\\.medienshop\\.lieferung').toggle();
    });
});
