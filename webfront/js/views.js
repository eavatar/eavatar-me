// views
avame.Views.Home = Backbone.View.extend({

    render: function () {
        var params = { message: "page one sub heading" };

        var template = _.template($("#homePage").html());
        $(this.el).html(template);
        console.log($(this.el))

        return this;
    },

    events: {
        "change #drpOne": "handleChange",
        "click #button1": "handleClick"
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

avame.Views.Notices = Backbone.View.extend({

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

avame.Views.Scripts = Backbone.View.extend({

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

avame.Views.Jobs = Backbone.View.extend({

    render: function () {
        var template = _.template($("#jobsPage").html());

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

avame.Views.Logs = Backbone.View.extend({

    render: function () {
        var template = _.template($("#logsPage").html());

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

avame.Views.Options = Backbone.View.extend({

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

avame.Views.About = Backbone.View.extend({

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

