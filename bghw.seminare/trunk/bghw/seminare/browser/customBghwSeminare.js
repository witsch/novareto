$(document).ready(function() {
    $('fieldset#pfg-fieldsetname-angaben-zur-ansprechperson').hide();
    $('div#archetypes-fieldname-beschreibung-der-funktion-im-betrieb').hide();

    var boolchecked = $('input#uebereinstimmung_2').attr('checked');

    if (boolchecked == true) {
        $('fieldset#pfg-fieldsetname-angaben-zur-ansprechperson').show();
    }

    $('input#uebereinstimmung_2').click(function() {
        $('fieldset#pfg-fieldsetname-angaben-zur-ansprechperson').fadeIn();
    })
    $('input#uebereinstimmung_1').click(function() {
        $('fieldset#pfg-fieldsetname-angaben-zur-ansprechperson').fadeOut();
    })
    $('input#berufliche-voraussetzungen_4').click(function() {
        $('div#archetypes-fieldname-beschreibung-der-funktion-im-betrieb').fadeIn();
    })
    $('input#berufliche-voraussetzungen_3').click(function() {
        $('div#archetypes-fieldname-beschreibung-der-funktion-im-betrieb').fadeOut();
    })
    $('input#berufliche-voraussetzungen_2').click(function() {
        $('div#archetypes-fieldname-beschreibung-der-funktion-im-betrieb').fadeOut();
    })
    $('input#berufliche-voraussetzungen_1').click(function() {
        $('div#archetypes-fieldname-beschreibung-der-funktion-im-betrieb').fadeOut();
    })
})

