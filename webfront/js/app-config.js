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
    api_base_url: '/api'
};


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