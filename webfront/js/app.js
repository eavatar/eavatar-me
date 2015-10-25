// main
avame.Router = Backbone.Router.extend({
    routes:{
        "":"home",
        "home": "home",
        "notices": "notices",
        "scripts": "scripts",
        "jobs": "jobs",
        "logs": "logs",
        "options": "options",
        "about": "about"
    },

    initialize: function () {
        console.log('initialize')
        this.firstPage = true;

        Backbone.history.start();
    },

    home: function () {

        console.log('routing to page1')

        this.changePage(new avame.Views.Home( {} ));

    },

    notices: function () {
        this.changePage(new avame.Views.Notices( {} ));
    },

    scripts: function () {
        this.changePage(new avame.Views.Scripts( {} ));
    },

    jobs: function () {
        this.changePage(new avame.Views.Jobs( {} ));
    },

    logs: function () {
        this.changePage(new avame.Views.Logs( {} ));
    },

    options: function () {
        this.changePage(new avame.Views.Options({}), 'pop');
    },

    about: function () {
        this.changePage(new avame.Views.About( {} ), 'pop');
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
        //$.mobile.changePage($(page.el), { reverse:false, changeHash:false, transition: transition });
    }
});

$(document).ready(function () {
    console.log('document ready');
    app = new avame.Router();
});

