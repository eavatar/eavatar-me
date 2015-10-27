
ava.models.Notice = Backbone.Model.extend({
    defaults: {
        kind: 'info',
        message: '',
        title: 'Ava Message'
    },

    initialize: function(){
    }
});

ava.models.NoticeCollection = Backbone.Collection.extend({
    model: ava.models.Notice,
    url: '/api/notices',
    parse: function(response){
        return response.data;
    }

});



ava.models.Job = Backbone.Model.extend({
    defaults: {
        st: '',
        name: '',
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
    url: '/api/jobs',
    parse: function(response){
        console.log("parse jobs response")
        return response.data;
    }

});


ava.models.Log = Backbone.Model.extend({

    defaults: {
        ts: 0,
        lvl: 20,
        lvl_name: 'INFO',
        msg: ''
    },

    initialize: function(entry) {
        if(entry == null) {
            return
        }

        this.set('ts', entry.ts)
        this.set('lvl', entry.lvl)
        this.set('msg', entry.msg)

        if(entry.lvl < 30) {
            this.set('lvl_name', 'INFO')
        } else if(entry.lvl < 40) {
            this.set('lvl_name', 'ALERT')
        } else {
            this.set('lvl_name', 'ERROR')
        }

    }
});

ava.models.LogCollection = Backbone.Collection.extend({
    model: ava.models.Log,
    url: '/api/logs',
    parse: function(response){
        console.log("parse logs response")
        return response.data;
    }
});




ava.models.Script = Backbone.Model.extend({
    defaults: {
        title: '',
        content: ''
    },

});

ava.models.ScriptCollection = Backbone.Collection.extend({
    model: ava.models.Script,
    url: '/api/scripts',
    parse: function(response){
        return response.data;
    }
});


ava.models.Session = Backbone.Model.extend( {
    defaults: {
        id: '1',
        token: null
    },

    url: '/api/auth',

    authenticated: function() {
        return this.get('token') != null
    },

    logout: function() {
        this.set('token', null)
    }
});

