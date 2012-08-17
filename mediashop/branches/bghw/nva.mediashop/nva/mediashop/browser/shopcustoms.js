jq(document).ready(function() {

    jq('#field_form_agb').children('label').replaceWith('<label><a target="_blank" href="http://www.bghw.de/medienangebot/allgemeine-geschaeftsbedingungen-agb">Hinweise zur Bestellung und Nutzung</a></label>&nbsp;<span class="fieldRequired" title="Required">(Required)</span>');

    jq('#field_form_datenschutz').children('label').append('<span class="fieldRequired" title="Required">(Required)</span>');

});
