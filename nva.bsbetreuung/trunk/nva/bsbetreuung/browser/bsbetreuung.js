jq(document).bind('ready', function() {

    if (jq('dl.portlet.portletErgebnisPortlet').length !=0) {
        var fixedwidth = jq('dl.portlet.portletDGUV2Help').width();
    }
    if (jq('dl.portlet.portletDGUV2Help').length != 0) {
        var xportlet = jq('dl.portlet.portletDGUV2Help').position().left;
        jq('dl.portlet.portletDGUV2Help').css({width:fixedwidth});
    }
    if (jq('fieldset#hh_fragen').length != 0) {
        var yfieldset = jq('fieldset#hh_fragen').position().top;
    }
    if (jq('input[value=ja]').length != 0) {
        var yyes = jq('input[value=ja]').position().top;
    }

    jq('fieldset#hh_fragen').hide();
    jq('div#nofields').hide();

    var boolchecked = jq("input#form\\.mybool\\.0").attr('checked');

    if (boolchecked == true) {
            jq('fieldset#hh_fragen').show();
            jq('dl.portlet.portletDGUV2Help').css({width:fixedwidth, position:"absolute", top:yfieldset, left:xportlet});
    }
    
    jq('input[value=nein]').bind('click', function() {
        jq('fieldset#hh_fragen').fadeOut();
        jq('div#nofields').fadeIn();
        jq('dl.portlet.portletDGUV2Help').css({width:fixedwidth, position:"absolute", top:yyes, left:xportlet});

     });

    jq('input[value=ja]').bind('click', function() {
        jq('div#nofields').fadeOut();
        jq('fieldset#hh_fragen').fadeIn();
        jq('dl.portlet.portletDGUV2Help').css({width:fixedwidth, position:"absolute", top:yfieldset, left:xportlet});
     });

    var helplinks = jq('a.hhportlet_help');
    jq(helplinks).click(function(event, data) {
        var myurl = event.currentTarget + "/helpwindow_view";
        window.open(myurl, 'Continue_to_Application', 'width=600, height=500, resizable=1');
        event.preventDefault();
    });

    var bshelplinks = jq('a.bs_help');
    jq(bshelplinks).click(function(event, data) {
        var myurl = event.currentTarget;
        window.open(myurl, 'Continue_to_Application', 'width=600, height=500, resizable=1');
        event.preventDefault();
    });

    jq.ajaxSetup({cache: false});

})    
