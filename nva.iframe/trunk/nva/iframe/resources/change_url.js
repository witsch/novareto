$(document).ready(function(){
    $('a').each(function(){
        this.href = this.href.replace('http://seminardatenbank.bgetem.de', 'http://www.bgetem.de/seminare/seminardatenbank-1/seminardatenbank');
        this.href = this.href.replace(';', '&DetailID=');
    });
});

