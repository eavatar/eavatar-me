// JQM config
$(document).on("mobileinit", function () {
    console.log('mobileinit')
    $.mobile.ajaxEnabled = false;
    $.mobile.linkBindingEnabled = false;
    $.mobile.hashListeningEnabled = false;
    $.mobile.pushStateEnabled = false;
    $.mobile.defaultPageTransition = "fade";
    $.mobile.autoInitializePage = false;
    //$.mobile.page.prototype.options.domCache = false;

    //$.mobile.phonegapNavigationEnabled = true;
    //$.mobile.page.prototype.options.degradeInputs.date = true;

    $("div[data-role='page']").on("pagehide", function (event, ui) {
        $(event.currentTarget).remove();
    });
});


