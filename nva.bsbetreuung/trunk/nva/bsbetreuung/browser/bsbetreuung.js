$(document).bind('ready', function() {

    /* $('span.required').empty(); */

    if ($('dl.portlet.portletErgebnisPortlet').length !=0) {
        var fixedwidth = $('dl.portlet.portletDGUV2Help').width();
    }
    if ($('dl.portlet.portletDGUV2Help').length != 0) {
        var xportlet = $('dl.portlet.portletDGUV2Help').position().left;
        $('dl.portlet.portletDGUV2Help').css({width:fixedwidth});
    }
    if ($('fieldset#hh_fragen').length != 0) {
        var yfieldset = $('fieldset#hh_fragen').position().top;
    }
    if ($('input[value=ja]').length != 0) {
        var yyes = $('input[value=ja]').position().top;
    }

    $('fieldset#hh_fragen').hide();
    $('div#nofields').hide();

    var boolchecked = $("input#form\\.mybool\\.0").attr('checked');

    if (boolchecked == 'checked') {
            $('fieldset#hh_fragen').show();
            $('dl.portlet.portletDGUV2Help').css({width:fixedwidth, position:"absolute", top:yfieldset, left:xportlet});
    }
    
    $('input[value=nein]').bind('click', function() {
        $('fieldset#hh_fragen').fadeOut();
        $('div#nofields').fadeIn();
        $('dl.portlet.portletDGUV2Help').css({width:fixedwidth, position:"absolute", top:yyes, left:xportlet});

     });

    $('input[value=ja]').bind('click', function() {
        $('div#nofields').fadeOut();
        $('fieldset#hh_fragen').fadeIn();
        $('dl.portlet.portletDGUV2Help').css({width:fixedwidth, position:"absolute", top:yfieldset, left:xportlet});
     });

    var helplinks = $('a.hhportlet_help');
    $(helplinks).click(function(event, data) {
        var myurl = event.currentTarget + "/helpwindow_view";
        window.open(myurl, 'Continue_to_Application', 'width=600, height=500, resizable=1');
        event.preventDefault();
    });

    var bshelplinks = $('a.bs_help');
    $(bshelplinks).click(function(event, data) {
        var myurl = event.currentTarget;
        window.open(myurl, 'Continue_to_Application', 'width=600, height=500, resizable=1');
        event.preventDefault();
    });

    $.ajaxSetup({cache: false});

})    
