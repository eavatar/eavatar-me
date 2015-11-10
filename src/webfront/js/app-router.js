// main
ava.router = Backbone.Router.extend({
    routes:{
        "":"about",
        "home": "console",
        "notices": "notices",
        "scripts": "scripts",
        "scriptEdit/:script_id": "scriptEdit",
        "jobs": "jobs",
        "jobs/:job_id/:action": "jobs",
        "logs": "logs",
        "console": "console",
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
            if(name != 'login' && name !='' && ava.session.get('token') == null) {
                console.log("Routing to page:", name)
                this.changePage(this.aboutPage);
                return
            }
            callback.apply(router, arguments);
        };
        return Backbone.Router.prototype.route.call(this, route, name, f);
    },

    initialize: function () {
        console.log('router.initialize')
        this.firstPage = true;
        this.currentPage = 'notices'
        ava.session = new ava.models.Session()

        this.consolePage = new ava.views.Console()
        this.noticeList = new ava.views.NoticeList()
        this.jobList = new ava.views.JobList()
        this.logList = new ava.views.LogList()
        this.scriptList = new ava.views.ScriptList()
        this.aboutPage = new ava.views.About()
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
        window.location.hash = 'console'
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

    console: function () {
        this.currentPage = 'console'
        this.changePage(this.consolePage);
    },

    notices: function () {
        this.currentPage = 'notices'
        // this.changePage(new ava.views.NoticeList({notices: this.notices}));
        this.noticeList.notices.fetch()
        this.changePage(this.noticeList)
    },

    scripts: function () {
        this.currentPage = 'scripts'
        this.scriptList.scripts.fetch()
        this.changePage(this.scriptList);
    },

    scriptEdit: function(script_id) {
        this.changePage(new ava.views.ScriptEdit(script_id));
    },

    jobs: function(job_id, action) {
        if(job_id === undefined || job_id === null) {
            this.currentPage = 'jobs'
            this.jobList.jobs.fetch()
            this.changePage(this.jobList);
            return
        }

        if(action === null) {
            action = 'view'
        }

        if(action == 'view') {
            this.currentPage = 'jobs/' + job_id + '/view'
            this.changePage(new ava.views.JobView(job_id, action))
        } else if(action == 'cancel') {
            this.changePage(new ava.views.JobView(job_id, action))
        }
    },

    logs: function () {
        this.currentPage = 'logs'
        this.logList.logs.fetch()
        this.changePage(this.logList);
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

