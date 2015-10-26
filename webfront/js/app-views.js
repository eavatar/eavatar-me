// views

ava.views.Header = Backbone.View.extend({
    render: function (params) {
        var template = _.template($("#header-template").html());
        $(this.el).html(template(params));

        return this;
    },
});

ava.views.Footer = Backbone.View.extend({
    render: function () {
        var template = _.template($("#footer-template").html());
        $(this.el).html(template);

        return this;
    },
});

ava.views.Home = Backbone.View.extend({

    render: function () {
        var params = { title: "EAvatar " + Math.random(),
            header: this.header,
            footer: this.footer
         };

        var template = _.template($("#homePage").html());
        $(this.el).html(template(params));

        return this;
    },

    events: {
        "change #drpOne": "handleChange",
        "submit #submit_form": "handleClick"
    },

    handleClick: function (e) {
        e.preventDefault();

        notify({
            type: "info",
            title: "Ava Message",
            message: "Super simple Notify plugin.",

            position: { x: "right", y: "top" },
            icon: '<img src="/img/paper_plane.png" />',
            size: "normal",
            overlay: false,
            closeBtn: true,
            overflowHide: false,
            spacing: 20,
            theme: "dark-theme",
            autoHide: true,
            delay: 2500,
            onShow: null,
            onClick: null,
            onHide: null,
            template: '<div class="notify"><div class="notify-text"></div></div>'

        });
    },

    handleChange: function (e) {
        e.preventDefault();

        var $this = $(e.target);

        alert($this.val());
    },

    initialize: function (options) {
        console.log('Home.initialize')

        _.bindAll(this, "render");
        header = new ava.views.Header()
        header.render({title: "EAvatar ME"})

        this.header = header.$el.html()
        footer = new ava.views.Footer()
        footer.render()
        this.footer = footer.$el.html()
        this.render();
    }
});

ava.views.Notices = Backbone.View.extend({

    render: function () {
        var params = { message: "page two sub heading" };

        var template = _.template($("#noticesPage").html());

        $(this.el).html(template);
        return this;
    },

    events: {
        "change #drpTwo": "handleChange",
        "click #button2": "handleClick"
    },

    handleClick: function (e) {
        e.preventDefault();

        alert("clicked");
    },

    handleChange: function (e) {
        e.preventDefault();

        var $this = $(e.target);

        alert($this.val());
    },

    initialize: function (options) {
        _.bindAll(this, "render");

        this.render();
    }
});

ava.views.Scripts = Backbone.View.extend({

    render: function () {
        var template = _.template($("#scriptsPage").html());

        $(this.el).html(template);
        return this;
    },

    events: {
        "change #drpTwo": "handleChange",
        "click #button2": "handleClick"
    },

    handleClick: function (e) {
        e.preventDefault();

        alert("clicked");
    },

    handleChange: function (e) {
        e.preventDefault();

        var $this = $(e.target);

        alert($this.val());
    },

    initialize: function (options) {
        _.bindAll(this, "render");

        this.render();
    }
});

ava.views.Jobs = Backbone.View.extend({

    render: function () {
        var template = _.template($("#jobsPage").html());

        $(this.el).html(template());
        return this;
    },

    events: {
        "change #drpTwo": "handleChange",
        "click #button2": "handleClick"
    },

    handleClick: function (e) {
        e.preventDefault();

        alert("clicked");
    },

    handleChange: function (e) {
        e.preventDefault();

        var $this = $(e.target);

        alert($this.val());
    },

    initialize: function (options) {
        _.bindAll(this, "render");

        this.render();
    }
});

ava.views.Logs = Backbone.View.extend({

    render: function () {
        var template = _.template($("#logsPage").html());
        //this.logs.fetch()
        console.log("Logs.render")
        data = this.logs.toJSON()
        this.$el.html(template({'logs': data}));
        $(this.el).trigger("create");  // trigger JQM to re-style the page

        return this;
    },

    events: {
        "change #drpTwo": "handleChange",
        "click #button2": "handleClick"
    },

    handleClick: function (e) {
        e.preventDefault();

        alert("clicked");
    },

    handleChange: function (e) {
        e.preventDefault();

        var $this = $(e.target);

        alert($this.val());
    },

    initialize: function (options) {
        _.bindAll(this, "render");
        this.logs = new ava.models.Logs()
        this.logs.fetch()
        this.logs.on('sync', this.render)
        //this.render();
    }
});

ava.views.Options = Backbone.View.extend({

    render: function () {
        var template = _.template($("#optionsPage").html());

        $(this.el).html(template);
        return this;
    },

    events: {
        "change #drpTwo": "handleChange",
        "click #button2": "handleClick"
    },

    handleClick: function (e) {
        e.preventDefault();

        alert("clicked");
    },

    handleChange: function (e) {
        e.preventDefault();

        var $this = $(e.target);

        alert($this.val());
    },

    initialize: function (options) {
        _.bindAll(this, "render");
        $(this.el).attr('data-dialog', 'true');

        this.render();
    }
});

ava.views.About = Backbone.View.extend({

    render: function () {
        var template = _.template($("#aboutPage").html());

        $(this.el).html(template);
        return this;
    },

    initialize: function (options) {
        _.bindAll(this, "render");
        $(this.el).attr('data-dialog', 'true');
        this.render();
    }
});

