_.templateSettings = {
    interpolate: /\{\{\=(.+?)\}\}/g,
    evaluate: /\{\{(.+?)\}\}/g
};

var ava = ava || {};

ava.router = null;
ava.views = {};
ava.models = {};
ava.config = {
    version: '0.1.0',
    api_base_url: '/api'
};


