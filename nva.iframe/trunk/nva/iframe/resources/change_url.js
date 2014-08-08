$(document).ready(function(){
    $('a').each(function(){
        this.href = this.href.replace('http://vedaentwicklung-etem.bg-kooperation.de', 'http://entwicklung-etem.bg-kooperation.de/seminare/vedaseminare');
        this.href = this.href.replace(';', '&DetailID=');
    });
});

