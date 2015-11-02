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
        $(this.el).html(template());

        return this;
    },
});

ava.views.Message = Backbone.View.extend({
    render: function () {
        var template = _.template($("#messageBox").html());
        params = {
            'message': this.message,
            'title': this.title
        }
        $(this.el).html(template(params));
        $(this.el).trigger("create");
        return this;
    },

    initialize: function(message, title) {
        console.log('Message.initialize')
        this.message = message || ''
        this.title = title || 'Message'
        $(this.el).attr('data-dialog', 'true');

        //this.render();
    }
});

ava.views.Confirm = Backbone.View.extend({
    render: function () {
        var template = _.template($("#confirmBox").html());
        params = {
            'message': this.message,
            'title': this.title
        }
        $(this.el).html(template(params));
        // $(this.el).trigger("create");
        return this;
    },

    events: {
            "click #yesBtn": "handleYesBtnClicked",
            "click #noBtn": "handleNoBtnClicked",
    },

    handleYesBtnClicked: function(e) {
        e.preventDefault();
        console.log("Yes button clicked.")
        console.log(this.callback)
        this.callback(true)
    },

    handleNoBtnClicked: function(e) {
        e.preventDefault();
        this.callback(false)
    },

    initialize: function(message, title, callback) {
        console.log('Confirm.initialize')
        this.message = message || ''
        this.title = title || 'Message'
        $(this.el).attr('data-dialog', 'true');
        $(this.el).attr('data-close-btn', 'none');
        this.confirmed = false
        this.callback = callback
        this.render();
    }
});

ava.views.Home = Backbone.View.extend({
    render: function () {
        var params = { title: "EAvatar " + Math.random(),
            header: this.header,
            footer: this.footer
         };

        var template = _.template($("#homePage").html());
        $(this.el).html(template(params));
        $(this.el).trigger("create");
        return this;
    },

    _show_message: function (msg) {
        $('#submit_message').text(msg)
    },

    events: {
        "click #clearBtn": "handleClear",
        "click #checkBtn": "handleCheck",
        "click #submitBtn": "handleSubmit"
    },

    handleClear: function (e) {
        console.log("Clear button clicked.")
        e.preventDefault();
        $('#script').val('')
    },

    handleCheck: function(e) {
        console.log("Check button clicked.")
        e.preventDefault();
        url = '/api/scripts/check'
        script = $('#script').val()
        if(_.isEmpty(script)) {
            this._show_message("Script is empty.")
            return
        }

        data = {
        }

        data['script'] = script
        console.log('script:', script)

        options = {
            contentType: 'application/json',
            success: _.bind(this._handle_check_success, this),
            error: _.bind(this._handle_check_error, this),
            type: 'POST',
            data: JSON.stringify(data)
        }

        $.ajax(url, options)
    },
    _handle_check_success: function(data,textStatus) {
        this._show_message("Check OK")
    },

    _handle_check_error: function(xhr,status,error) {
        this._show_message("Error: " + error);
    },

    handleSubmit: function (e) {
        console.log("Submit button clicked.")
        e.preventDefault();
        url = '/api/jobs';

        script = $('#script').val()
        if(_.isEmpty(script)) {
            console.log("No script content")
            return
        }

        data = {
        }

        data['script'] = script
        console.log('script:', script)

        options = {
            contentType: 'application/json',
            success: this.submission_succeeded,
            error: this.submission_failed,
            type: 'POST',
            data: JSON.stringify(data)
        }

        $.ajax(url, options)
    },

    submission_succeeded: function(data,textStatus) {
        console.log("Job submission succeeded.")
        $('#submit_message').html('Job submitted successfully. Job ID = ' + data['data'])
        $('#script').val('')
    },

    submission_failed: function(xhr,status,error) {
        console.log("Job submission failed:", error)
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

ava.views.NoticeList = Backbone.View.extend({

    render: function () {
        data = this.notices.toJSON()
        var params = {
            header: this.header,
            footer: this.footer,
            notices: data
         };

        var template = _.template($("#noticesPage").html());

        $(this.el).html(template(params));
        $(this.el).trigger("create");
        return this;
    },

    initialize: function (options) {
        _.bindAll(this, "render");
        this.notices = new ava.models.NoticeCollection()
        this.notices.on('sync', this.render)

        header = new ava.views.Header()
        header.render({title: "User Notices"})
        this.header = header.$el.html()
        footer = new ava.views.Footer()
        footer.render()
        this.footer = footer.$el.html()

        this.render();
    }
});

ava.views.ScriptList = Backbone.View.extend({

    render: function () {
        data = this.scripts.toJSON();
        var params = {
            header: this.header,
            footer: this.footer,
            scripts: data
         };

        var template = _.template($("#scriptsPage").html());
        $(this.el).html(template(params));

        $(this.el).html(template(params));
        $(this.el).trigger("create");
        return this;
    },

    initialize: function (options) {
        _.bindAll(this, "render");
        this.scripts = new ava.models.ScriptCollection()
        this.scripts.on('sync', this.render)

        header = new ava.views.Header()
        header.render({title: "Job Scripts"})
        this.header = header.$el.html()
        footer = new ava.views.Footer()
        footer.render()
        this.footer = footer.$el.html()

        this.render();
    }
});

ava.views.ScriptEdit = Backbone.View.extend({

    render: function () {
        var template = _.template($("#scriptEditPage").html());
        params = {model: this.model}
        $(this.el).html(template(params));
        $(this.el).trigger("create");

        return this;
    },

    events: {
        "click #okBtn": "handleOK",
        "click #cancelBtn": "handleCancel"
    },


    handleOK: function (e) {
        e.preventDefault();

    },

    handleCancel: function (e) {
        e.preventDefault();

    },

    initialize: function (script_id) {
        _.bindAll(this, "render");
        $(this.el).attr('data-dialog', 'true');

        console.log("Edit script:", script_id)
        this.script_id = script_id
        this.model = new ava.models.Script({id: script_id})
        this.model.on('sync', this.render, this)
        //this.render();
    }
});

ava.views.JobList = Backbone.View.extend({

    render: function () {
        data = this.jobs.toJSON()

        var params = {
            header: this.header,
            footer: this.footer,
            'jobs': data
         };

        var template = _.template($("#jobsPage").html());
        this.$el.html(template(params));
        $(this.el).trigger("create");  // trigger JQM to re-style the page
        return this;
    },

    initialize: function () {
        _.bindAll(this, "render");
        this.jobs = new ava.models.JobCollection()
        this.jobs.on('sync', this.render)

        header = new ava.views.Header()
        header.render({title: "Running Jobs"})
        this.header = header.$el.html()
        footer = new ava.views.Footer()
        footer.render()
        this.footer = footer.$el.html()
        // this.render();
    }
});

ava.views.JobView = Backbone.View.extend({


    render: function () {
        data = this.job.toJSON()

        var params = {
            header: this.header,
            footer: this.footer,
            'job': data
         };

        var template = _.template($("#jobDetailsPage").html());
        this.$el.html(template(params));
        $(this.el).trigger("create");  // trigger JQM to re-style the page
        return this;
    },

    initialize: function (job_id, action) {

        if(action == 'cancel') {
            job = new ava.models.Job({id: job_id})
            job.destroy()
            window.location.hash = '#jobs'
            return
        }

        _.bindAll(this, "render");
        this.job = new ava.models.Job({id: job_id})
        this.job.fetch()
        this.job.on('sync', this.render)

        header = new ava.views.Header()
        header.render({title: "Job Info"})
        this.header = header.$el.html()
        footer = new ava.views.Footer()
        footer.render()
        this.footer = footer.$el.html()
        // this.render();
    }
});

ava.views.LogList = Backbone.View.extend({

    render: function () {
        data = this.logs.toJSON()

        var params = {
            header: this.header,
            footer: this.footer,
            'logs': data
         };

        var template = _.template($("#logsPage").html());
        //this.logs.fetch()
        this.$el.html(template(params));
        $(this.el).trigger("create");  // trigger JQM to re-style the page

        return this;
    },

    initialize: function (options) {
        _.bindAll(this, "render");
        header = new ava.views.Header()
        header.render({title: "Recent Logs"})
        this.header = header.$el.html()
        footer = new ava.views.Footer()
        footer.render()
        this.footer = footer.$el.html()

        this.logs = new ava.models.LogCollection()
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
        msg = ava.config.flash_message;
        var params = {
            'flash_message': msg
         };

        ava.config.flash_message = '';
        var template = _.template($("#aboutPage").html());

        $(this.el).html(template(params));
        return this;
    },

    events: {
        "submit": "handleSubmit"
    },

    handleSubmit: function(e) {
        console.log("Login submit")
        e.preventDefault();
        token = $('#token').val()
        ava.session.set('token', token)
        ava.session.fetch()
        window.location.hash = 'home'
    },


    initialize: function (options) {
        _.bindAll(this, "render");
        $(this.el).attr('data-dialog', 'true');
        $(this.el).attr('data-close-btn', 'none');

        this.render();
    }
});

