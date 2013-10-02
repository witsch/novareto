jq (document).ready(function() {
    jq('fieldset#pfg-fieldsetname-angaben-zur-ansprechperson').hide();
    jq('div#archetypes-fieldname-beschreibung-der-funktion-im-betrieb').hide();

    var boolchecked = jq('input#uebereinstimmung_2').attr('checked');

    if (boolchecked == true) {
        jq('fieldset#pfg-fieldsetname-angaben-zur-ansprechperson').show();
    }

    jq('input#uebereinstimmung_2').click(function() {
        jq('fieldset#pfg-fieldsetname-angaben-zur-ansprechperson').fadeIn();
    })
    jq('input#uebereinstimmung_1').click(function() {
        jq('fieldset#pfg-fieldsetname-angaben-zur-ansprechperson').fadeOut();
    })
    jq('input#berufliche-voraussetzungen_4').click(function() {
        jq('div#archetypes-fieldname-beschreibung-der-funktion-im-betrieb').fadeIn();
    })
    jq('input#berufliche-voraussetzungen_3').click(function() {
        jq('div#archetypes-fieldname-beschreibung-der-funktion-im-betrieb').fadeOut();
    })
    jq('input#berufliche-voraussetzungen_2').click(function() {
        jq('div#archetypes-fieldname-beschreibung-der-funktion-im-betrieb').fadeOut();
    })
    jq('input#berufliche-voraussetzungen_1').click(function() {
        jq('div#archetypes-fieldname-beschreibung-der-funktion-im-betrieb').fadeOut();
    })
})

