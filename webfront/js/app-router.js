// main
ava.router = Backbone.Router.extend({
    routes:{
        "":"about",
        "home": "home",
        "notices": "notices",
        "scripts": "scripts",
        "jobs": "jobs",
        "logs": "logs",
        "options": "options",
        "login/:token": "login",
        "logout": "logout",
        "denied": "denied",
        "*other" : "about"
    },

    route: function(route, name, callback) {
        var router = this;
        if (!callback) callback = this[name];

        var f = function() {
            // check token existence for all except 'login' page.
            if(name != 'login' && ava.session.get('token') == null) {
                this.changePage(new ava.views.About());
                return
            }
            callback.apply(router, arguments);
        };
        return Backbone.Router.prototype.route.call(this, route, name, f);
    },

    initialize: function () {
        console.log('router.initialize')
        this.firstPage = true;
        this.currentPage = 'home'
        ava.session = new ava.models.Session()
    },

    message: function(message, title) {
        this.changePage(new ava.views.Message(message, title), 'pop');
    },

    confirm: function(message, title, callback) {
        this.changePage(new ava.views.Confirm(message, title, callback), 'pop');
    },

    login: function(token) {
        console.log("router.login")
        ava.session.set('token', token)
        ava.session.fetch()
        window.location.hash = 'home'
    },

    logout: function() {
        callback = $.proxy(this.logoutConfirm, this)
        this.confirm("Do you really want to log out?", "Are you sure?", callback)
    },

    logoutConfirm: function(confirmed) {
        if(confirmed) {
            ava.session.logout()
            this.message("You have logged out successfully.")
        } else {
            window.location.hash = this.currentPage
        }
    },

    denied: function() {
        this.message("Authorization is required to access.", "Access Denied")
    },

    home: function () {
        this.currentPage = 'home'
        this.changePage(new ava.views.Home());
    },

    notices: function () {
        this.currentPage = 'notices'
        this.changePage(new ava.views.NoticeList( {} ));
    },

    scripts: function () {
        this.currentPage = 'scripts'
        this.changePage(new ava.views.ScriptList( {} ));
    },

    jobs: function () {
        this.currentPage = 'jobs'
        this.changePage(new ava.views.JobList( {} ));
    },

    logs: function () {
        this.currentPage = 'logs'
        this.changePage(new ava.views.LogList( {} ));
    },

    options: function () {
        this.currentPage = 'options'
        this.changePage(new ava.views.Options({}), 'pop');
    },

    about: function () {
        this.changePage(new ava.views.About( {} ));
    },

    defaultRoute: function() {

    },


    changePage:function (page, transition) {
        $(page.el).attr('data-role', 'page');

        page.render();

        // console.log('page.el', $(page.el))
        $('body').append(page.$el);

        var transition = transition || $.mobile.defaultPageTransition;

        // We don't want to fade the first page. Slide, and risk the annoying "jump to top".
        if (this.firstPage) {
            transition = "none";
            $.mobile.initializePage();
            this.firstPage = false;
        }
        $(":mobile-pagecontainer").pagecontainer( "change", $(page.el),
                { changeHash: false, transition: transition });
    }
});

$(document).ready(function () {
    console.log('document ready');
    app = new ava.router();
    Backbone.history.start();

});

