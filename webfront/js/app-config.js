_.templateSettings = {
    interpolate: /\{\{\=(.+?)\}\}/g,
    evaluate: /\{\{(.+?)\}\}/g
};

var ava = ava || {};

ava.router = null;
ava.views = {};
ava.models = {};
ava.session = {};
ava.config = {
    version: '0.1.0',
    base_url: '',
    flash_message: ''
};

ava.eventBus = _.extend({}, Backbone.Events);



$.ajaxSetup({
    statusCode: {
        401: function(){
            // Redirec the to the login page.
            window.location.replace('/#denied');

        },
        403: function() {
            // 403 -- Access denied
            window.location.replace('/#denied');
        }
    },

    beforeSend: function(req) {
        req.setRequestHeader('Authorization', ava.session.get('token'));
    }
});