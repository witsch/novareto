$(document).ready(function(){
    $('a').each(function(){
        this.href = this.href.replace('http://10.10.60.154:8080/WebGate_test', 'http://entwicklung-etem.bg-kooperation.de/seminare/vedaseminare');
        this.href = this.href.replace(';', '&DetailID=');
    });
});

