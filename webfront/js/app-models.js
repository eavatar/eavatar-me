
ava.models.Notice = Backbone.Model.extend({
    defaults: {
        kind: 1,
        priority: 'info',
        message: '',
        title: 'Ava Message'
    },

    urlRoot: function() {
        return ava.config.base_url + '/api/notices'
    },

    parse: function(response){
        return response.data;
    },

    initialize: function(entry){
        if(entry == null) {
            return
        }

        if(entry.priority < 30) {
            this.set('priority', 'info')
        } else if(entry.lvl < 40) {
            this.set('priority', 'alert')
        } else {
            this.set('priority', 'error')
        }

        this.set('id', entry.id)
        this.set('kind', entry.kind)
        this.set('title',  entry.title)
        this.set('message', entry.message)
        this.set('timestamp', entry.timestamp)
    }
});

ava.models.NoticeCollection = Backbone.Collection.extend({
    model: ava.models.Notice,
    url: function() {
        return ava.config.base_url + '/api/notices'
    },
    parse: function(response){
        return response.data;
    }

});



ava.models.Job = Backbone.Model.extend({
    defaults: {
        st: '',
        name: '',
    },

    urlRoot: function() {
        return ava.config.base_url + '/api/jobs'
    },

    parse: function(response){
        return response.data;
    },

    initialize: function(entry) {
        if(entry == null) {
            return
        }
        this.set('st',  entry.st)
        this.set('name', entry.name)
        this.set('id', entry.id)
    }
});

ava.models.JobCollection = Backbone.Collection.extend({
    model: ava.models.Job,
    url: function() {
        return ava.config.base_url + '/api/jobs'
    },

    parse: function(response){
        return response.data;
    }

});


ava.models.Log = Backbone.Model.extend({

    defaults: {
        ts: 0,
        lvl: 20,
        lvl_name: 'info',
        msg: ''
    },

    urlRoot: function() {
        return ava.config.base_url + '/api/logs'
    },

    parse: function(response){
        return response.data;
    },


    initialize: function(entry) {
        if(entry == null) {
            return
        }

        this.set('ts', entry.ts)
        this.set('lvl', entry.lvl)

        if(entry.msg.length > 256) {
            entry.msg = entry.msg.substring(0, 256)
        }
        this.set('msg', entry.msg)

        if(entry.lvl < 30) {
            this.set('lvl_name', 'info')
        } else if(entry.lvl < 40) {
            this.set('lvl_name', 'alert')
        } else {
            this.set('lvl_name', 'error')
        }

    }
});

ava.models.LogCollection = Backbone.Collection.extend({
    model: ava.models.Log,
    url: function() {
        return ava.config.base_url + '/api/logs';
    },
    parse: function(response){
        console.log("parse logs response");
        return response.data;
    }
});




ava.models.Script = Backbone.Model.extend({
    defaults: {
        title: '',
        text: ''
    },
    urlRoot: function() {
        return ava.config.base_url + '/api/scripts'
    },

    parse: function(response){
        return response.data;
    },

    initialize: function(entry) {
        if(entry == null) {
            return
        }

        this.set('id', entry.id)
        this.set('title', entry.title)
        this.set('text', entry.text)

    }
});

ava.models.ScriptCollection = Backbone.Collection.extend({
    model: ava.models.Script,
    url: function() {
        return ava.config.base_url + '/api/scripts'
    },
    parse: function(response){
        return response.data;
    }
});


ava.models.Session = Backbone.Model.extend( {
    defaults: {
        id: '1',
        token: null
    },

    url: function() {
        return ava.config.base_url + '/api/auth'
    },

    authenticated: function() {
        return this.get('token') != null
    },

    logout: function() {
        this.set('token', null)
    }
});

